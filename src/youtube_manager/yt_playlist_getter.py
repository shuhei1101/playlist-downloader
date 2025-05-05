import logging
from typing import Callable
import yt_dlp

import config
from domain.playlist import Playlist

class YtPlaylistGetter:
    async def get(self, playlist_url,
                  on_error: Callable[[Exception], None] = None,
                  ) -> Playlist:
        '''プレイリストのURLから動画のURLを配列で取得する'''
        try:
            ydl_opts = {
                'quiet': True,
                'extract_flat': True,
                'skip_download': True,
                'logger': logging.getLogger('yt_dlp'),
                'logtostderr': False,
            }
            logging.getLogger('yt_dlp').setLevel(config.YT_DLP_LOG_LEVEL)  # ログレベルをERRORに設定

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(playlist_url, download=False)
                
                return Playlist.from_info(info)
        except Exception as e:
            on_error(e)

# 動作確認用
if __name__ == "__main__":
    import asyncio
    try:
        playlist = asyncio.run(YtPlaylistGetter().get(
            playlist_url='https://www.youtube.com/@shimabu_it/videos'
            ))
        print("\n".join(playlist.urls))
        print(f"タイトル: {playlist.title}")
        print(f"動画数: {len(playlist.urls)}")
    except ValueError as e:
        print()
