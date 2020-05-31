import requests
from bs4 import BeautifulSoup

url = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'

q = requests.get(url)
if q.status_code == 200:
    soup = BeautifulSoup(q.text, features='lxml')
    table = soup.find('table', {'class': 'h4'})
    stock = []
    for i in table.children:
        all_data = [k.text for k in i.find_all('td')]
        if len(all_data) == 7:
            stock.append(all_data[0].split('\u3000')[0])
    stock = [i for i in stock if len(i) == 4]
    print(len(stock))
    # table = soup.find_all('table')[1]
    # get_all = table.find_all(class_='xl24')
    # new_stocks = [re.findall('>(\d+)<span', str(i))[0] for i in get_all if re.findall('>(\d+)<span', str(i))]
    # new_stocks = [i for i in new_stocks if len(i) == 4]
    # print(new_stocks)
