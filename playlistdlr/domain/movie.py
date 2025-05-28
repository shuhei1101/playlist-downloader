from dataclasses import dataclass

from playlistdlr import config
from util.converter import sanitize_filename


@dataclass
class Movie:
    id: str
    url: str
    title: str

    @classmethod
    def from_entry(cls, entry: dict) -> "Movie":
        """yt-dlpのエントリからMovieオブジェクトを生成"""
        title = sanitize_filename(entry["title"])
        if config.HAS_UPLOAD_DATE:
            title = f"{entry['upload_date']}_{title}"
        return cls(
            id=entry["id"],
            url=entry["url"],
            title=title,
        )

    def is_private(self) -> bool:
        """プライベート動画かどうかを判定

        titleが[Private video]で始まる場合はプライベート動画とみなす
        """
        return self.title.startswith("[Private video]")
