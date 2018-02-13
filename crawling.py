import requests
from bs4 import BeautifulSoup
import os
import time
from random import random
from tqdm import tqdm
import pdb


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


def all_crowling(category: str=""):
    """
    カテゴリ内のすべての
    検索ページのHTMLを引き抜いてくる
    category: URLで使われているカテゴリ名
    """

    with open("prefectures.txt", "r") as f:
        prefectures = f.readline().split("\n")
    # 都道府県ごとにスクレイピング
    for pref in tqdm(prefectures):
        print(pref)
        url = "https://itp.ne.jp/" + pref + "/genre_dir/" + category + "/pg/"
        pref_dir = dir_name + pref + "/"
        make_dir(pref_dir)
        crowling_to_prefecture(url, pref_dir)


def crowling_to_prefecture(baseurl: str="", pref_dir: str=""):
    """
    都道府県ごとにカテゴリ内の検索ページの
    HTMLを取得し，テキストファイルに保存
    baseurl  : TownPageのURL
    pref_dir : テキストファイルを保存するディレクトリ
    """

    # 都道府県のindexは0~9 * 10 + 1~5 で決まっている
    for i in tqdm(range(0, 10)):
        for j in range(1, 6):
            k = 1
            idx = i * 10 + j
            while k < 101:
                nexttime = time.time() + 10 + random()
                # htmlをクローリング
                url = baseurl + str(k) + "/?nad=1&sr=1&st=4&evdc=1&idx=" + str(idx)
                req = requests.get(url, headers={"User-Agent": agent})
                content = req.content
                soup = BeautifulSoup(content, "html.parser")
                # 10s+a だけ待つ
                time.sleep(nexttime - time.time())
                # 何も情報がなければwhileを抜ける
                if not soup.find(class_="noResult") is None:
                    break
                # テキストに保持
                with open(pref_dir + str(idx) + "_" + str(k) + ".html", "w") as f:
                    f.write(str(soup))
                k += 1


def main():
    global dir_name
    global agent
    # カテゴリを指定
    category = "sweets"
    dir_name = category + "_search_pages/"
    # ユーザーエージェントを指定
    agent = "Mozilla/5.0 (Linux; Android 4.0.3; SC-02C Build/IML74K) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.58 Mobile Safari/537.31"
    # 保持用のディレクトリを作成
    make_dir(dir_name)
    # クローリング開始
    all_crowling(category)


if __name__ == "__main__":
    main()
