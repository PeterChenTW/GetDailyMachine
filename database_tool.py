import configparser
import os

import mysql.connector


class StockDB:
    config = configparser.ConfigParser()
    config.read(f'{os.path.abspath(os.path.dirname(__file__))}/config.ini')
    mysql_info = config['mysql']

    def connection(self):
        self.cnx = mysql.connector.connect(user=self.mysql_info['user'],
                                           password=self.mysql_info['password'],
                                           host=self.mysql_info['host'],
                                           database=self.mysql_info['database'])

    def close_connection(self):
        self.cnx.close()

    def once_insert_into_stock_history(self, txt_path):
        cursor = self.cnx.cursor()
        sql = (f"LOAD DATA INFILE '{txt_path}' INTO TABLE `stock_history`"
               f"FIELDS TERMINATED BY ',';")
        cursor.execute(sql)
        self.cnx.commit()
        cursor.close()

    def insert_into_stock_history(self, broker_index, stock, price, buy, sell, date):
        """
        :param broker_index: int
        :param stock: int
        :param price: float
        :param buy: int
        :param sell: int
        :param date: datetime
        :return:
        """
        data = {
            'broker_index': broker_index,
            'stock': stock,
            'price': price,
            'buy': buy,
            'sell': sell,
            'date': date
        }
        cursor = self.cnx.cursor()
        add_stock_history = ("INSERT INTO stock_history "
                             "(broker_index, stock, price, buy, sell, date) "
                             "VALUES (%(broker_index)s, %(stock)s, %(price)s, %(buy)s, %(sell)s, %(date)s)")
        cursor.execute(add_stock_history, data)
        self.cnx.commit()
        cursor.close()

    def insert_into_broker(self, index, broker):
        data = {
            'index': index,
            'broker': broker
        }
        cursor = self.cnx.cursor()
        add_broker = ("INSERT INTO `broker` "
                      "(`index`, `broker`) "
                      "VALUES (%(index)s, %(broker)s)")
        cursor.execute(add_broker, data)
        self.cnx.commit()
        cursor.close()

    def select_broker_index_exist(self, broker_index):
        cursor = self.cnx.cursor()
        select_index = ("SELECT EXISTS (SELECT `index` FROM `broker` "
                        "WHERE `index` = %s)")
        cursor.execute(select_index, (broker_index,))
        ans = [i[0] for i in cursor][0]
        cursor.close()
        return ans

    def init_table(self):
        actions = [
            "CREATE TABLE `stock_history` ("
            "  `index` int(11) NOT NULL AUTO_INCREMENT,"
            "  `broker_index` varchar(11) NOT NULL,"
            "  `stock` int(11) NOT NULL,"
            "  `price` float(14) NOT NULL,"
            "  `buy` int(11) NOT NULL,"
            "  `sell` int(11) NOT NULL,"
            "  `date` date NOT NULL,"
            "  PRIMARY KEY (`index`)"
            ") ENGINE=InnoDB",

            "CREATE INDEX `stock*broker_index` ON stock_history (`stock`, `broker_index`)",

            "CREATE TABLE `broker` ("
            "  `index` varchar(11) NOT NULL,"
            "  `broker` varchar(11) NOT NULL,"
            "  PRIMARY KEY (`index`),"
            "  UNIQUE (`index`)"
            ") ENGINE=InnoDB"
        ]

        cursor = self.cnx.cursor()
        for action in actions:
            cursor.execute(action)
        cursor.close()


if __name__ == '__main__':
    DB = StockDB()
    DB.connection()
    DB.init_table()
    # DB.insert_into_broker(1112, 'e04su3')
    # print(DB.select_broker_index_exist(12))
    # from datetime import date
    # DB.insert_into_stock_history(111, 2330, 11.0, 1100, 0, date(2000, 6, 4))
    DB.close_connection()
