# -*- coding:utf-8 -*-
import logging
import os
import time
from random import random

import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor

df = pd.read_csv('F:/pywork/有序.csv', encoding='gbk',dtype={'secCode': str})


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
secName = df.loc[:, "secCode"]

with ThreadPoolExecutor(max_workers=8) as pool:
    with requests.Session() as s:
        futures = [pool.submit(get_announcement, s, url, secName) for url, secName in zip(url, secName)]
