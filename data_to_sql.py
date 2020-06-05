import pandas as pd
import re
from collections import deque


def parse_deal(deal):
    if not deal[0]:
        return None
    broker_index = re.findall('([a-zA-Z0-9]+)', deal[1])[0]
    broker = deal[1].split(broker_index)[1]
    price = float(deal[2])
    buy = int(deal[3])
    sell = int(deal[4])
    return broker_index, broker, price, buy, sell

def deal_data(file_path):
    with open(file_path, 'r', encoding='Big5-HKSCS') as fp:
        context = fp.read().split('\n')
        stock_id = re.findall('="(\d+)"', context[1])[0]
        deal_history = deque()
        for i in context[3:]:
            deals = i.replace('\u3000', '').split(',')
            if len(deals) == 1:
                continue
            deal_1, deal_2 = deals[:5], deals[-5:]
            deal_history.append(parse_deal(deal_1))
            deal_history.append(parse_deal(deal_2))
    return stock_id, deal_history


from database_tool import StockDB
DB = StockDB()
DB.connection()

import os

for i in os.listdir('daily/2020-06-02'):
    stock_id, deal_history = deal_data(f'daily/2020-06-02/{i}')
    for deal in deal_history:
        if deal is None:
            continue
        broker_index, broker, price, buy, sell = deal
        DB.insert_into_stock_history(broker_index, stock_id, price, buy, sell, '2020-06-02')
