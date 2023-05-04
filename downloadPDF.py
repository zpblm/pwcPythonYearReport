# -*- coding:utf-8 -*-
import logging
import os
import time
from random import random

import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor

df = pd.read_csv('F:/pywork/深沪京2022年报1.csv', encoding='gbk',dtype={'secCode': str})
# 按日期降序排序
df = df.sort_values(['announcementTime'], ascending=False)
# 以最新年报作为结果
df = df.groupby(['secName']).agg('first').reset_index()

def get_announcement(s, url, secName):
    try:
        r = s.get(url)
        filename = str(secName) + ".pdf"
        print(filename)
        with open(filename, 'wb') as f:
            f.write(r.content)
    except Exception as e:
        logging.warning(secName, e)
        time.sleep(random.random() * 5)


os.chdir("年报PDF")
url = df.loc[:, "adjunctUrl"]
secName = df.loc[:, "announcementTitle"]

with ThreadPoolExecutor(max_workers=8) as pool:
    with requests.Session() as s:
        futures = [pool.submit(get_announcement, s, url, secName) for url, secName in zip(url, secName)]
