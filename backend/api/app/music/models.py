import io

from pydantic import BaseModel


class SongBase(BaseModel):
    artist: str
    song_title: str


class Song(SongBase):
    filename: str


class SongPacket(Song):
    buffer: bytes
