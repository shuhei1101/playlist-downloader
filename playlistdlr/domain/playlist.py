from dataclasses import dataclass

from domain.movie import Movie


@dataclass
class Playlist:
    title: str
    movies: list[Movie]

    @classmethod
    def from_info(cls, info: dict) -> 'Playlist':
        '''yt-dlpのエントリからPlaylistオブジェクトを生成'''
        return cls(
            title=info['title'],
            movies=[Movie.from_entry(entry) for entry in info['entries']]
        )
