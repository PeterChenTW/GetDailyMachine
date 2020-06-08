import pandas as pd
import re
from collections import deque


def parse_deal(deal, stock_id, date):
    if not deal[0]:
        return None
    broker_index = re.findall('([a-zA-Z0-9]+)', deal[1])[0]
    # broker = deal[1].split(broker_index)[1]
    price = deal[2]
    buy = deal[3]
    sell = deal[4]
    return broker_index, stock_id, price, buy, sell, date


def deal_data(file_path, date):
    with open(file_path, 'r', encoding='Big5-HKSCS') as fp:
        context = fp.read().split('\n')
        stock_id = re.findall('="(\d+)"', context[1])[0]
        deal_history = deque()
        for i in context[3:]:
            deals = i.replace('\u3000', '').split(',')
            if len(deals) == 1:
                continue
            deal_1, deal_2 = deals[:5], deals[-5:]
            deal_history.append(parse_deal(deal_1, stock_id, date))
            deal_history.append(parse_deal(deal_2, stock_id, date))
    deal_history = [i for i in deal_history if i is not None]
    return deal_history

import sqlalchemy
sqlEngine = sqlalchemy.create_engine('mysql+mysqlconnector://root:password@127.0.0.1/stock')

dbConnection = sqlEngine.connect()
# from database_tool import StockDB
# DB = StockDB()
# DB.connection()

import os
deal_date = '2020-06-02'
tmp_list = []
for i in os.listdir(f'daily/{deal_date}'):
    if i[:4] != 'excd':
        tmp_list += deal_data(f'daily/{deal_date}/{i}', deal_date)
    print(i, 'done')
import time
s_time = time.time()
deal_history = pd.DataFrame(tmp_list, columns=['broker_index', 'stock_id', 'price', 'buy', 'sell', 'date'])
deal_history.to_sql('stock_history', dbConnection, if_exists='append')
e_time = time.time()
print(e_time - s_time)
# print(len(tmp_list))
# tmp_str = '\n'.join(tmp_list)
# with open('tmp_workplace/tmp.txt', 'w') as file:
#     file.writelines(tmp_str)
#
#
# DB.once_insert_into_stock_history('tmp_workplace/tmp.txt')
