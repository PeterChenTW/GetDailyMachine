import configparser
import os
import re
from collections import deque

import pandas as pd
import sqlalchemy

config = configparser.ConfigParser()
config.read('config.ini')
mysql_info = config['mysql']


# base function
def connection():
    engine = sqlalchemy.create_engine(
        f"mysql+mysqlconnector://{mysql_info['user']}:{mysql_info['password']}@{mysql_info['host']}/{mysql_info['database']}")
    db_con = engine.connect()
    return db_con


# save data to mysql
def data_to_mysql(deal_date):
    try:
        db_con = connection()

        tmp_list = []
        for stock in os.listdir(f'daily/{deal_date}'):
            if stock[:4] != 'excd':
                tmp_list += deal_data(f'daily/{deal_date}/{stock}', deal_date)

        deal_history = pd.DataFrame(tmp_list, columns=['broker_index', 'stock', 'price', 'buy', 'sell', 'date'])
        deal_history.to_sql('stock_history', db_con, if_exists='append', index=False)
        db_con.close()
    except Exception as e:
        print(f'error: {e}')


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


def parse_deal(deal, stock_id, date):
    if not deal[0]:
        return None
    broker_index = re.findall('([a-zA-Z0-9]+)', deal[1])[0]
    # broker = deal[1].split(broker_index)[1]
    price = deal[2]
    buy = deal[3]
    sell = deal[4]
    return broker_index, stock_id, price, buy, sell, date


# select data from mysql

db_con = connection()
sql = "select * from stock_history where stock = 2330"
df = pd.read_sql_query(sql, db_con)
print(df)
