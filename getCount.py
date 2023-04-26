import time

import wencai as wc
import pandas as pd
from wencai.core.session import Session

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('expand_frame_repr', False)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

Session.headers.update({'Host' : 'www.iwencai.com'})

wc.set_variable(cn_col=True)

all_data = pd.DataFrame()
i = 1
# 52是来自http://www.iwencai.com/unifiedwap/result?w=%E5%B8%82%E5%80%BC&querytype=stock&addSign=1682474739668
while i <= 52:
    try:
        data = wc.search('市值', page = i)
        all_data = all_data._append(data, ignore_index=True)
        i = i + 1
    except:
        print("第" + i + '页爬取被拦截，等待3秒后重试~')
        time.sleep(3)
def drop_shszbj(c):
    return c.replace('.SH', '').replace('SZ', '').replace('.BJ', '')
all_data.loc[:, '股票代码'] = all_data.loc[:, '股票代码'].apply(lambda c: drop_shszbj(c))
df = all_data[['股票简称', '股票代码', '总市值', '所属同花顺行业']]
df.to_csv('F:/pywork/市值及行业.csv', index=False, encoding='utf_8_sig')

