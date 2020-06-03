import mysql.connector

cnx = mysql.connector.connect(user='root', password='password',
                              host='localhost', database='stock')

actions = []
actions.append(
    "CREATE TABLE `stock_history` ("
    "  `index` int(11) NOT NULL AUTO_INCREMENT,"
    "  `stock` int(11) NOT NULL,"
    "  `broker_index` int(11) NOT NULL,"
    "  `price` float(14) NOT NULL,"
    "  `buy` int(11) NOT NULL,"
    "  `sell` int(11) NOT NULL,"
    "  `date` date NOT NULL,"
    "  PRIMARY KEY (`index`)"
    ") ENGINE=InnoDB"
)
actions.append(
    "CREATE INDEX `stock*broker_index` ON stock_history (`stock`, `broker_index`)"
)

actions.append(
    "CREATE TABLE `broker` ("
    "  `index` int(11) NOT NULL,"
    "  `broker` int(11) NOT NULL,"
    "  PRIMARY KEY (`index`)"
    ") ENGINE=InnoDB"
)

cursor = cnx.cursor()
for action in actions:
    cursor.execute((action))
cursor.close()
cnx.close()
