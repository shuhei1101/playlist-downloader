import logging
import os


# ========================== 使用者用設定 ==========================
# 保存対象のプレイリストやチャンネル（動画タブ）のURLを指定
TARGET_PAGES = [
    # フェルミ
    # "https://www.youtube.com/playlist?list=PL0BlYtzX4pz_xA5Gu98Q48C8-y0Q0c7Ch",
    # 彰人アナザーボーカル
    "https://www.youtube.com/playlist?list=PLWJxNkBs5XIJYQS4ngIZK1oFL9T-LP2VK",
    # "https://www.youtube.com/playlist?list=PLa2arPD_RzYOy0Eo1dK2zWYX6PUzdSeQ5",
]

# 保存形式（mp4, mp3, all)
# SAVE_FORMAT = "mp4"
SAVE_FORMAT = "mp3"
# SAVE_FORMAT = "all"


# youtube api
# API_KEY = ""


# ========================== 開発者用設定 ==========================
# ---------------- ログ設定 ----------------
APP_LOG_LEVEL = logging.DEBUG  # アプリケーションのログレベル設定
APP_LOG_PATH = os.path.join(
    os.getenv("LOG_DIR"), "app.log"
)  # アプリケーションのログファイルパス
YT_DLP_LOG_LEVEL = logging.CRITICAL  # yt_dlpのログレベル設定


# ---------------- バリデーションチェック ----------------
# 保存形式の確認
if SAVE_FORMAT not in ["mp4", "mp3", "all"]:
    raise ValueError(
        f"不明な保存形式`{SAVE_FORMAT}`が指定されました。config.pyを確認してください。"
    )
