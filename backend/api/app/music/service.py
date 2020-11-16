import io
import pickle
from typing import List

from app.core.aws import session
from app.core.config import AppConfig
from app.core.queue import JobQueue
from app.music.models import Song, SongPacket
from app.cache.service import CacheService
from app.storage.service import StorageService
from app.opus.parser import OpusParser


class SongService:

    __dynamodb = session.resource('dynamodb')
    __table = __dynamodb.Table(AppConfig.MUSIC_TABLE_NAME)
    __song_iter = None


    @classmethod
    def __get_song_iterator(cls):
        last_evaluated_key = None
        response = cls.__table.scan(Limit=1, Select="ALL_ATTRIBUTES")

        while response["Items"]:
            last_evaluated_key = response["LastEvaluatedKey"]
            song = response["Items"][0]
            
            yield Song(**song)

            response = cls.__table.scan(
                Limit=1,
                Select="ALL_ATTRIBUTES",
                ExclusiveStartKey=last_evaluated_key
            )


    @classmethod
    def __get_next_song(cls) -> Song:
        try:
            song = next(cls.__song_iter)
        except (StopIteration, TypeError):
            cls.__song_iter = cls.__get_song_iterator()
            song = next(cls.__song_iter)
        return song


    @classmethod
    def __get_song_bytes(cls, song: Song) -> bytes:
        buffer = CacheService.get(song.filename)

        if buffer is None:
            stream = StorageService.get_byte_stream(f"music/{song.filename}")
            buffer = stream.getbuffer()
            CacheService.set(song.filename, buffer)
        
        return buffer


    @classmethod
    def preload_next_song(cls):
        seq_max = int(CacheService.get("seq_max") or 0)
        seq_base = int(CacheService.get("seq_base") or 0)

        song = cls.__get_next_song()
        buffer = cls.__get_song_bytes(song)
        parser = OpusParser(buffer)

        seq_base = seq_max + 1

        while packet := parser.get_next_packet():
            seq_max += 1
            CacheService.set(
                f"song:packet:{seq_max}", 
                pickle.dumps(
                    SongPacket(**song.dict(), buffer=packet.read())
                )
            )

        CacheService.set("seq_base", seq_base)
        CacheService.set("seq_max", seq_max)


    @classmethod
    def init(cls):
        if not int(CacheService.get("seq_max") or 0):
            JobQueue.enqueue(SongService.preload_next_song)


class MusicService:

    @staticmethod
    def get_next_audio_packet(seq: int = None):
        seq_base = int(CacheService.get("seq_base"))
        seq_max = int(CacheService.get("seq_max"))
        
        if not seq:
            seq = seq_base

        if seq > (seq_max - 10):
            JobQueue.enqueue(SongService.preload_next_song)
        
        packet = pickle.loads(CacheService.get(f"song:packet:{seq}"))

        return packet
