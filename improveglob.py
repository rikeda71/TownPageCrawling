# -*- coding: utf-8 -*-
import re
import glob

"""
glob.globの結果をソートして返すためのモジュール
数字は数字の大きさ順にソートされる
"""


def sort_glob(path):
    """
    path : フォルダ名
    """
    return sorted(glob.glob(path), key=__numerical_sort)


def __numerical_sort(value):
    """
    数字の順番を考慮したソートでファイル名を取得
    """
    numbers = re.compile(r"(\d+)")
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
