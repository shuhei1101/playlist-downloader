import os


def has_partial_filename(dir: str, keyword: str) -> bool:
    """
    指定フォルダ内で、ファイル名にキーワードが部分一致するものがあるかを判定する関数。

    Parameters:
        folder_path (str): フォルダのパス
        keyword (str): 検索キーワード（部分一致）

    Returns:
        bool: 一致するファイルが1つでもあれば True、なければ False
    """
    try:
        files = os.listdir(dir)
        return any(keyword in f for f in files)
    except FileNotFoundError:
        print("フォルダが見つかりません:", dir)
        return False


# 動作確認用
if __name__ == "__main__":
    dir_path = "/Users/nishikawashuhei/nishikawa/30_repos/playlist-downloader/tmp"
    keyword = "test.txt"
    print(f"ディレクトリ: {dir_path}, キーワード: {keyword}")
    result = has_partial_filename(dir=dir_path, keyword=keyword)
    print("部分一致するファイルが存在するか:", result)
