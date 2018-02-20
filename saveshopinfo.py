from bs4 import BeautifulSoup
from improveglob import sort_glob
from makedir import make_dir
import pandas as pd


def extract_infomation(text: str=""):
    """
    HTMLから書かれている情報を抽出する
    店名，郵便番号，住所，電話番号, URL, メールアドレス
    text : HTMLの内容
    """

    soup = BeautifulSoup(text, "html.parser")
    shops = ([s.text.replace("詳細", "").replace("\n", "") for s in soup.find_all(class_="row titleRow")])
    urls = []
    emails = []
    postalcodes = []
    addresses = []
    telnumbers = []
    idx = 0

    # 郵便番号，住所，電話番号, URL, e-mailを保存
    for s in soup.find_all("dl")[10:]:
        details = s.find_all("dt")
        info = s.find_all("dd")
        urls.append("")
        emails.append("")
        postalcodes.append("")
        addresses.append("")
        telnumbers.append("")
        for i in range(len(details)):
            # 郵便番号と住所を保存
            if str(details[i]) == "<dt>【住所】</dt>":
                # 郵便番号と住所を分割し保存
                codes = info[i].text.split(" ")
                postalcodes[idx] = codes[0]
                addresses[idx] = codes[1]
            # 電話番号を保存
            elif str(details[i]) == "<dt>【電話番号】</dt>":
                telnumbers[idx] = info[i].text
            # お店のURLを保存
            elif str(details[i]) == "<dt>【URL】</dt>":
                urls[idx] = info[i].text
            # メールアドレスを保存
            elif str(details[i]) == "<dt>【e-mail】</dt>":
                emails[idx] = info[i].text
        idx += 1
    return shops, postalcodes, addresses, telnumbers, urls, emails


def pref_save_shopinfo(path: str):
    """
    指定した都道府県のお店・企業の情報を保存する
    path : 都道府県のディレクトリ
    """

    data = []
    shops = []
    urls = []
    emails = []
    postalcodes = []
    addresses = []
    telnumbers = []

    # HTMLに書かれているお店・企業の情報を抽出する
    for filedir in sort_glob(path + "/*"):
        # print(filedir)
        with open(filedir, "r") as f:
            text = f.read()
        info = extract_infomation(text)
        shops.extend(info[0])
        postalcodes.extend(info[1])
        addresses.extend(info[2])
        telnumbers.extend(info[3])
        urls.extend(info[4])
        emails.extend(info[5])

    # pandasの形式に変換してcsvに保存
    for (s, p, a, t, u, e) in zip(shops, postalcodes, addresses, telnumbers, urls, emails):
        data.append([s, p, a, t, u, e])
    df = pd.DataFrame(data,
                      columns=["name", "postalcode", "address", "telnumber", "url", "email"])
    df.to_csv(directory + "/" + path[path.index("/"):] + ".csv", index=False)


def all_save_shopinfo(paths: str):
    """
    カテゴリ内の情報を保存する
    paths : カテゴリのディレクトリ
    """

    # 情報を保持するディレクトリを作成
    make_dir(directory)
    # 都道府県ごとに情報を保存
    for prefdir in sort_glob(paths + "/*"):
        pref_save_shopinfo(prefdir)


def main():
    global directory
    category = "sweets"
    paths = category + "_search_pages"
    directory = category + "_shop_info"
    all_save_shopinfo(paths)


if __name__ == "__main__":
    main()
