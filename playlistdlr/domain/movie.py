from dataclasses import dataclass

from util.converter import sanitize_filename


@dataclass
class Movie:
    id: str
    url: str
    title: str

    @classmethod
    def from_entry(cls, entry: dict) -> "Movie":
        """yt-dlpのエントリからMovieオブジェクトを生成"""
        return cls(
            id=entry["id"], url=entry["url"], title=sanitize_filename(entry["title"])
        )

    def is_private(self) -> bool:
        """プライベート動画かどうかを判定

        titleが[Private video]で始まる場合はプライベート動画とみなす
        """
        return self.title.startswith("[Private video]")
