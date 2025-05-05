import asyncio
from typing import Callable
import yt_dlp

from domain.movie import Movie
from util.converter import remove_playlist
from youtube_manager.ydl_opts_builder import YdlOptsBuilder, YdlOptsFormat


class YtDownloader:
    '''YouTube動画をダウンロードするクラス'''

    async def download(self, movie: Movie, filename: str, builder: YdlOptsBuilder,
                       on_success: Callable[[Movie, str], None],
                       on_error: Callable[[Exception, Movie, str], None],
                       ):
        try:
            # 非同期で同期的な処理を実行
            await asyncio.to_thread(self._sync_download, remove_playlist(movie.url), builder.build())
            on_success(movie, filename)
        except Exception as e:
            on_error(e, movie, filename)

    def _sync_download(self, url, ydl_opts):
        '''同期的なダウンロード処理'''
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

async def test():
    import config
    downloader = YtDownloader()
    DL_MP4_TASK = asyncio.create_task(downloader.download(
        url="https://www.youtube.com/watch?v=2NxC8pRSGkQ&list=PLa2arPD_RzYMkyLssxnLE3JPQ9MbP_vtH&index=3",
        builder=YdlOptsBuilder() \
            .set_output_dir(config.OUTPUT_DIR) \
            .set_filename("%(title)s.%(ext)s") \
            .set_format(YdlOptsFormat.MP4),
        on_error=None
    ))

    await DL_MP4_TASK

# 動作確認用
if __name__ == "__main__":
    import asyncio
    asyncio.run(test())


