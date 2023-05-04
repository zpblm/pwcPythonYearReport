import logging
import math
import time

import pandas as pd
import requests
from datetime import datetime

url = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
headers = {
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
    "Connection": "keep-alive"
}


def get_json(pageNum, s):
    """ 获取list的json数据
    :param pageNum: 页数
    :param s:session
    :return: json data

        'seDate': '2022-12-31~2023-04-10', 95页
        'seDate': '2023-04-11~2023-04-23', 90页
        'seDate': '2023-04-24~2023-04-27', 97页
        'seDate': '2023-04-28~2023-05-30', 76页
    """

    params = {
        'pageSize': '30',
        'column': 'szse',
        'tabName': 'fulltext',
        'category': 'category_ndbg_szsh',
        'seDate': '2022-12-31~2023-05-30',
        'isHLtitle': 'true'
    }

    params['pageNum'] = str(pageNum)
    try:
        res = s.post(url, headers=headers, params=params)
        print(str(pageNum) + "页爬取完成~")
    except Exception as e:
        logging.warning(e)
    return res.json()


with requests.Session() as s:
    json1 = get_json(1, s)
    page_one = pd.DataFrame(json1['announcements'])
    max_num_page = json1['totalRecordNum']

column = page_one.columns
max_page = math.ceil(max_num_page/30)
print('最大页数：'+str(max_page))

pages = range(1, max_page+1)
myJosn = []


for i in pages:
    json = get_json(i, s)
    time.sleep(0.1)
    announcements_list = json['announcements']
    items = []
    for item in announcements_list:
        if str(item['secName']) not in str(item['announcementTitle']):
            item['announcementTitle'] = item['secName'] + item['announcementTitle']
        item['announcementTitle'] = item['announcementTitle'].replace('*', '')
        if ('摘要' not in str(item['announcementTitle'])) and ('2022' in str(item['announcementTitle'])) and ('英文版' not in str(item['announcementTitle'])):
            items.append(item)
    myJosn.extend(pd.DataFrame(items).values)

res_df = pd.DataFrame(myJosn, columns=column)
res_df.head()
res_df.info()
raw_data = res_df.drop(
    columns=['id', 'announcementId', 'adjunctSize', 'adjunctType', 'storageTime', 'columnId', 'pageColumn',
             'secNameList',
             'announcementType', 'associateAnnouncement', 'important', 'batchNum', 'orgName', 'announcementTypeName',
             'announcementContent', 'tileSecName', 'shortTitle'],
)


def drop_em(c):
    return c.replace('<em>', '').replace('</em>', '')


data_drop_em = raw_data.copy()
data_drop_em.loc[:, 'announcementTitle'] = data_drop_em.loc[:, 'announcementTitle'].apply(lambda c: drop_em(c))

data_drop_em.head()
# 将时间戳转化为日期
def transform_date(timeStamp):
    timeStamp = int(str(timeStamp)[:-3])
    timeArray = time.localtime(timeStamp)
    return time.strftime("%Y-%m-%d", timeArray)

data_time_transformed = data_drop_em.copy()
data_time_transformed.loc[:, 'announcementTime'] = data_time_transformed.loc[:, 'announcementTime'].apply(lambda c: transform_date(c))
data_time_transformed.head()


# 拼接pdf的url
def url_join(c):
    return ''.join(['http://static.cninfo.com.cn/', c])


data_url_joined = data_time_transformed.copy()
data_url_joined.loc[:, 'adjunctUrl'] = data_url_joined.loc[:, 'adjunctUrl'].apply(lambda c: url_join(c))
data_url_joined.head()

# 巨潮网只能一次爬取100页（3000条左右），所以请根据时间段，分别爬取2个CSV文件深沪京2022年报1.csv和深沪京2022年报2.csv，然后手动将其合并成一个
data_url_joined.to_csv('F:/pywork/深沪京2022年报99.csv', index=False, encoding='utf_8_sig')
