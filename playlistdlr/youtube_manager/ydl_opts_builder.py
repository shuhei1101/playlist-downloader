from enum import Enum, auto
import logging
import os


class YdlOptsFormat(Enum):
    MP4 = auto()
    MP3 = auto()


class YdlOptsBuilder:
    def __init__(self):
        self.format = ""
        self.postprocesors = ""
        self.output_dir = ""
        self.filename = ""

    def build(self) -> dict:
        """設定を辞書形式で返す

        :raise ValueError: 出力先のテンプレートが設定されていない場合
        :return: 設定を辞書形式で返す
        """
        # バリデーションチェック
        if not self.output_dir and not self.filename:
            raise ValueError("output_dirとfilenameのいずれかは必須です。")

        return {
            "quiet": True,
            "extract_flat": True,
            "logger": logging.getLogger("yt_dlp"),
            "logtostderr": True,
            "format": self.format,
            "outtmpl": os.path.join(self.output_dir, self.filename),
            "postprocessors": self.postprocesors,
        }

    def set_outtmpl(
        self, output_dir=os.getenv("OUTPUT_DIR"), filename="%(title)s.%(ext)s"
    ) -> "YdlOptsBuilder":
        """出力先のテンプレートを設定

        :param output_dir: 出力先のディレクトリ(デフォルトはos.getenv("OUTPUT_DIR"))
        :param filename: 出力ファイル名のテンプレート(デフォルトは"%(title)s.%(ext)s")
        """
        self.outtpml = os.path.join(output_dir, filename)  # type: ignore
        return self

    def set_output_dir(self, output_dir: str) -> "YdlOptsBuilder":
        """出力先のディレクトリを設定

        :param output_dir: 出力先のディレクトリ
        """
        self.output_dir = output_dir
        return self

    def set_filename(self, filename: str) -> "YdlOptsBuilder":
        """出力ファイル名のテンプレートを設定

        :param filename: 出力ファイル名のテンプレート
        """
        self.filename = filename
        return self

    def set_format(self, fmt: YdlOptsFormat) -> "YdlOptsBuilder":
        """出力フォーマットを設定"""
        if fmt == YdlOptsFormat.MP3:
            # MP3形式の場合
            self.format = "bestaudio"
            self.postprocesors = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ]
        elif fmt == YdlOptsFormat.MP4:
            # MP4形式の場合
            self.format = "best[ext=mp4]"
        else:
            raise ValueError("不正なフォーマットです")
        return self
