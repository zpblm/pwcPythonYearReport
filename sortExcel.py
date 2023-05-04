import pandas as pd


df = pd.read_csv('F:/pywork/2023-05-03.csv', encoding='gbk',dtype={'secCode': str})
# 按日期降序排序
df = df.sort_values(['announcementTime'], ascending=False)
# 以最新年报作为结果
df = df.groupby(['secName']).agg('first').reset_index()

df.to_csv('F:/pywork/有序.csv', index=False, encoding='utf_8_sig')
