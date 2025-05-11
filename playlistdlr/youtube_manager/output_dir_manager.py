import os
from typing import Callable


class OutputDirManager:
    """出力する動画の保存先を管理するクラス"""

    def __init__(self, dir_name: str):
        output_dir = self._get_output_dir(dir_name)
        self.mp3_dir = os.path.join(output_dir, "mp3")
        self.mp4_dir = os.path.join(output_dir, "mp4")

    def get_mp3_dir(self) -> str:
        return self.mp3_dir

    def get_mp4_dir(self) -> str:
        return self.mp4_dir

    @staticmethod
    def crean_dir(
        clean_dir: str,
        on_remove_dir: Callable[[str], None],
    ):
        """OUTPUT配下の空のディレクトリを削除する"""
        for root, dirs, _ in os.walk(clean_dir):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    on_remove_dir(dir_path)

    def _get_output_dir(self, dir_name) -> str:
        """出力先のディレクトリを作成して、そのパスを返す"""
        return os.path.join(os.getenv("OUTPUT_DIR"), dir_name)
