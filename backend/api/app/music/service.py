import io
from typing import List

import boto3

from app.core.config import AppConfig
from app.music.models import Song
from app.cache.service import CacheService
from app.storage.service import StorageService


class MusicService:

    __dynamodb = boto3.resource('dynamodb')
    __table = __dynamodb.Table(AppConfig.MUSIC_TABLE_NAME)
    __song_iter = None


    @classmethod
    def __get_song_iterator(cls) -> Song:
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
    def __get_next_song(cls):
        try:
            song = next(cls.__song_iter)
        except (StopIteration, TypeError):
            cls.__song_iter = cls.__get_song_iterator()
            song = next(cls.__song_iter)
        return song


    @classmethod
    def __get_song_byte_stream(cls, song: Song) -> io.BytesIO:
        stream = CacheService.get(song.filename)
        
        if stream is not None:
            return stream
        
        try:
            stream = StorageService.get_byte_stream(f"music/{song.filename}")
            CacheService.set(song.filename, stream.read())
            stream.seek(0)
        except FileNotFoundError as error:
            print(error)
            raise

        return stream
            