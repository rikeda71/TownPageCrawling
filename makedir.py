import os


def make_dir(path: str=""):
    """
    ディレクトリを作成
    例外処理によって既にディレクトリがあっても処理が終わらない
    path : 作成したいディレクトリのパス
    """
    try:
        os.mkdir(path)
    except:
        print(path + " already exists")
