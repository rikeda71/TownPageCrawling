import pandas as pd
import glob
import re
import mojimoji as moji


"""
店名のリストを作成する
"""


def makeshoplist(directory: str=""):
    """
    directory : shoplistを作りたいファイルが格納されているディレクトリ

    directory内のファイルをすべて参照し，ショップの名前リストを作る
    """

    # 都道府県の店名リストをすべて格納
    shoplist = [name for filename in glob.glob(directory + "/*") for name in get_shoplist_pref(filename)]
    # 単一出現かつソートを行う
    shoplist = sorted(list(set(shoplist)))
    # 〇〇店のような重複を削除する
    distance = -1
    for i in range(1, len(shoplist)):
        if shoplist[distance] in shoplist[i] and\
                ((len(shoplist[i]) - len(shoplist[distance])) > 2 or
                 shoplist[i][-1] == "店"):
            shoplist[i] = " "
        elif shoplist[i - 1] in shoplist[i] and\
                ((len(shoplist[i]) - len(shoplist[i - 1])) > 2 or
                 shoplist[i][-1] == "店"):
            shoplist[i] = " "
            distance = i - 1
        else:
            distance = -1

    # 保存
    savename = directory[:directory.find("_")] + "_shops.txt"
    with open(savename, "w") as f:
        f.write("\n".join([shop for shop in shoplist if shop != " "]))


def get_shoplist_pref(filedir: str=""):
    """
    filedir : 都道府県ごとの店情報が格納されたテキストファイルの場所

    1つの都道府県に関して，店の名前のリストを作成し，返す
    """

    shoplist = []
    contents = pd.read_csv(filedir)
    ltd = re.compile(r"([(株式)(有限)(合資)]+会社){1}")
    bracket = re.compile(r"\(.+\)")
    for shopname in contents["name"]:
        # カタカナ以外の文字を半角へ
        shopname = moji.zen_to_han(shopname, kana=False)
        # 括弧に囲まれた文字列を削除
        shopname = bracket.sub("", shopname)
        # 〇〇会社という文字列は除く
        shopname = ltd.sub("", shopname)
        # ／で区切られていたら区切られる前の文字列と
        # 区切り文字を消した文字列を格納する
        if shopname.find("/") > -1:
            shoplist.append(shopname[:shopname.find("/")])
            shopname = shopname.replace("/", "")
        shoplist.append(shopname)
    return shoplist


def main():
    makeshoplist("sweets_shop_info")


if __name__ == "__main__":
    main()
