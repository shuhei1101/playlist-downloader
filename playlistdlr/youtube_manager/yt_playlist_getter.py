import logging
from typing import Callable
import yt_dlp

from playlistdlr import config
from playlistdlr.domain.playlist import Playlist


class YtPlaylistGetter:
    async def get(
        self,
        playlist_url,
        on_error: Callable[[Exception], None] = None,  # type: ignore
    ) -> Playlist:  # type: ignore
        """プレイリストのURLから動画のURLを配列で取得する"""
        try:
            ydl_opts = {
                "quiet": True,
                "extract_flat": True,
                "skip_download": True,
                "logger": logging.getLogger("yt_dlp"),
                "logtostderr": False,
            }
            logging.getLogger("yt_dlp").setLevel(
                config.YT_DLP_LOG_LEVEL
            )  # ログレベルをERRORに設定

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(playlist_url, download=False)

                return Playlist.from_info(info)  # type: ignore
        except Exception as e:
            on_error(e)
