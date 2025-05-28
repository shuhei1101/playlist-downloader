def remove_playlist(yt_url: str) -> str:
    """
    プレイリストのURLを削除する関数
    :param yt_url: プレイリストのURL（httpsxxx&list=xxx）
    :return: プレイリストのURLを削除したURL（&list=以降を削除）
    """
    # プレイリストのURLを削除
    if "&list=" in yt_url:
        yt_url = yt_url.split("&list=")[0]
    return yt_url


def sanitize_filename(filename: str) -> str:
    # ファイル名に使用できない文字を置換
    result = filename.replace("\u3000", " ").replace("/", "／")
    return result


# 動作確認用
if __name__ == "__main__":
    filename = "【要約】ゆるストイック ── ノイズに邪魔されず１日を積み上げる思考【佐藤航陽】.mp4"
    print(filename)
    print(sanitize_filename(filename))
