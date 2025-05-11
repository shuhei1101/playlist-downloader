import os
import asyncio

from playlistdlr import config
from playlistdlr.app_logger import AppLogger
from playlistdlr.app_timer import AppTimer
from playlistdlr.domain.movie import Movie
from playlistdlr.youtube_manager.output_dir_manager import OutputDirManager
from playlistdlr.youtube_manager.ydl_opts_builder import YdlOptsBuilder, YdlOptsFormat
from playlistdlr.youtube_manager.yt_downloader import YtDownloader
from playlistdlr.youtube_manager.yt_playlist_getter import YtPlaylistGetter


async def main(logger=AppLogger()):
    try:
        main_timer = AppTimer.init_and_start()

        # プレイリストオブジェクトを取得
        tasks = [
            YtPlaylistGetter().get(
                playlist_url=url,
                on_error=lambda e: logger.error(
                    f"プレイリストの取得に失敗しました。URL: {url}, エラー: {_e_to_json(e)}"
                ),
            )
            for url in config.TARGET_PAGES
        ]
        playlists = await asyncio.gather(*tasks)

        # プレイリストの取得に失敗した場合は処理を中止
        if any(playlist is None for playlist in playlists):
            logger.error("プレイリストを一件も取得できませんでした。処理を中止します。")
            return

        # output配下の空のディレクトリを削除
        OutputDirManager.crean_dir(
            clean_dir=os.getenv("OUTPUT_DIR"),
            on_remove_dir=lambda dir_path: logger.debug(
                f"空のディレクトリ`{os.path.basename(dir_path)}`を削除しました。"
            ),
        )

        logger.info("ダウンロードの準備中...")

        completed = 0

        def on_success(movie: Movie, filename: str):
            nonlocal completed
            completed += 1
            logger.info(
                f"進捗: {completed}/{total}, ファイル: {filename}, URL: {movie.url}"
            )

        def on_error(e: Exception, movie: Movie, filename: str):
            nonlocal completed
            completed += 1
            logger.error(
                f"進捗: {completed}/{total}, ファイル: {filename}, URL: {movie.url}, エラー: {_e_to_json(e)}"
            )

        tasks = []
        for playlist in playlists:
            dir_manager = OutputDirManager(dir_name=playlist.title)

            for movie in playlist.movies:
                # private動画はスキップ
                if movie.is_private():
                    logger.info(f"スキップ: 非公開動画です。url: {movie.url}")
                    continue
                # MP4とMP3のダウンロードタスクを作成
                if config.SAVE_FORMAT in ["all", "mp4"]:
                    file_name = f"{movie.title}.mp4"
                    file_dir = dir_manager.get_mp4_dir()
                    file_path = os.path.join(file_dir, file_name)
                    if os.path.exists(file_path):
                        # ファイルが存在する場合はスキップ
                        logger.info(
                            f"スキップ: ファイル`{file_name}`は既に存在します。"
                        )
                    else:
                        os.makedirs(file_dir, exist_ok=True)
                        logger.info(
                            f"DL準備: ファイル: `{file_name}`, URL: `{movie.url}`"
                        )
                        DL_MP4_TASK = asyncio.create_task(
                            YtDownloader().download(
                                movie=movie,
                                filename=file_name,
                                builder=YdlOptsBuilder()
                                .set_output_dir(file_dir)
                                .set_filename(file_name)
                                .set_format(YdlOptsFormat.MP4),
                                on_success=on_success,
                                on_error=on_error,
                            )
                        )
                        tasks.append(DL_MP4_TASK)

                if config.SAVE_FORMAT in ["all", "mp3"]:

                    file_name = f"{movie.title}.mp3"
                    file_dir = dir_manager.get_mp3_dir()
                    file_path = os.path.join(file_dir, file_name)
                    if os.path.exists(file_path):
                        # ファイルが存在する場合はスキップ
                        logger.info(
                            f"スキップ: ファイル`{file_name}`は既に存在します。"
                        )
                    else:
                        os.makedirs(file_dir, exist_ok=True)
                        logger.info(
                            f"DL準備: ファイル: `{file_name}`, URL: `{movie.url}`"
                        )
                        DL_MP3_TASK = asyncio.create_task(
                            YtDownloader().download(
                                movie=movie,
                                filename=file_name,
                                builder=YdlOptsBuilder()
                                .set_output_dir(
                                    file_dir
                                )  # .mp3は自動で拡張子を付与してくれるので、タイトルのみを指定
                                .set_filename(movie.title)
                                .set_format(YdlOptsFormat.MP3),
                                on_success=on_success,
                                on_error=on_error,
                            )
                        )
                        tasks.append(DL_MP3_TASK)

        # 全てのダウンロードタスクを非同期で実行
        total = len(tasks)
        await asyncio.gather(*tasks)
        logger.info(
            f"ダウンロードが完了しました。実行時間: {main_timer.get_elapsed_time()}秒"
        )

    except Exception as e:
        logger.error(f"予期しないエラーが発生しました。エラー: {_e_to_json(e)}")
        logger.error("処理を中止します。")
        return


def _e_to_json(e: Exception) -> str:
    """エラーを一行のJSON形式に変換する"""
    tb = e.__traceback__
    line_number = tb.tb_lineno if tb else "N/A"
    file_name = tb.tb_frame.f_code.co_filename if tb else "N/A"
    return f'{{"error": "{str(e)}", "file": "{file_name}", "line": {line_number}}}'


if __name__ == "__main__":
    asyncio.run(main())
