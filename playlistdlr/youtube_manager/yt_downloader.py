import asyncio
from typing import Callable
import yt_dlp

from playlistdlr.domain.movie import Movie
from playlistdlr.util.converter import remove_playlist
from playlistdlr.youtube_manager.ydl_opts_builder import YdlOptsBuilder


class YtDownloader:
    """YouTube動画をダウンロードするクラス"""

    async def download(
        self,
        movie: Movie,
        filename: str,
        builder: YdlOptsBuilder,
        on_success: Callable[[Movie, str], None],
        on_error: Callable[[Exception, Movie, str], None],
    ):
        try:
            # 非同期で同期的な処理を実行
            await asyncio.to_thread(
                self._sync_download, remove_playlist(movie.url), builder.build()
            )
            on_success(movie, filename)
        except Exception as e:
            on_error(e, movie, filename)

    def _sync_download(self, url, ydl_opts):
        """同期的なダウンロード処理"""
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
