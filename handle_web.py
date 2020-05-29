import datetime
import os
import re
import shutil
import time

import cv2
import numpy as np
import pyautogui
import pytesseract
import requests
from bs4 import BeautifulSoup
from pyautogui import locateOnScreen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# setting
class GetDailyMachine:
    stock_url = 'https://bsr.twse.com.tw/bshtm/'
    py_path = os.path.abspath(os.path.dirname(__file__))
    download_path = '/Users/yushi.chen/Downloads'
    captcha_pic_path = f'{download_path}/CaptchaImage.jpeg'
    today = str(datetime.date.today())
    daily_path = f'{py_path}/daily/{today}'
    pic_path = py_path + '/pic'

    driver = None
    stocks = ['1101', '1102', '1103', '1104', '1107', '1109', '1110', '1201', '1203', '1204', '1207', '1210', '1212',
              '1213', '1215', '1216', '1217', '1218', '1219', '1220', '1221', '1224', '1225', '1227', '1228', '1229',
              '1231', '1232', '1233', '1234', '1235', '1236', '1301', '1303', '1304', '1305', '1306', '1307', '1308',
              '1309', '1310', '1311', '1312', '1313', '1314', '1315', '1316', '1319', '1321', '1323', '1324', '1325',
              '1326', '1402', '1407', '1408', '1409', '1410', '1413', '1414', '1416', '1417', '1418', '1419', '1423',
              '1432', '1434', '1435', '1436', '1437', '1438', '1439', '1440', '1441', '1442', '1443', '1444', '1445',
              '1446', '1447', '1449', '1450', '1451', '1452', '1453', '1454', '1455', '1456', '1457', '1458', '1459',
              '1460', '1462', '1463', '1464', '1465', '1466', '1467', '1468', '1469', '1470', '1471', '1472', '1473',
              '1474', '1475', '1476', '1477', '1503', '1504', '1506', '1507', '1510', '1512', '1513', '1514', '1515',
              '1516', '1517', '1519', '1520', '1521', '1522', '1523', '1524', '1525', '1526', '1527', '1528', '1529',
              '1530', '1531', '1532', '1533', '1534', '1535', '1536', '1537', '1538', '1539', '1540', '1541', '1601',
              '1602', '1603', '1604', '1605', '1606', '1608', '1609', '1611', '1612', '1613', '1614', '1615', '1616',
              '1617', '1618', '1701', '1702', '1704', '1707', '1708', '1709', '1710', '1711', '1712', '1713', '1714',
              '1715', '1716', '1717', '1718', '1720', '1721', '1722', '1723', '1724', '1725', '1726', '1727', '1729',
              '1730', '1731', '1732', '1733', '1734', '1735', '1736', '2002', '2006', '2007', '2008', '2009', '2010',
              '2012', '2013', '2014', '2015', '2017', '2020', '2022', '2023', '2024', '2025', '2027', '2028', '2029',
              '2030', '2031', '2032', '2033', '2034', '2101', '2102', '2103', '2104', '2105', '2106', '2107', '2108',
              '2109', '2201', '2204', '2206', '2207', '2301', '2302', '2303', '2305', '2308', '2310', '2311', '2312',
              '2313', '2314', '2315', '2316', '2317', '2318', '2319', '2321', '2322', '2323', '2324', '2325', '2326',
              '2327', '2328', '2329', '2330', '2331', '2332', '2333', '2335', '2336', '2337', '2338', '2339', '2340',
              '2341', '2342', '2343', '2344', '2345', '2347', '2348', '2349', '2350', '2351', '2352', '2353', '2354',
              '2355', '2356', '2357', '2358', '2359', '2360', '2361', '2362', '2363', '2364', '2365', '2366', '2367',
              '2368', '2369', '2370', '2371', '2373', '2374', '2375', '2376', '2377', '2378', '2379', '2380', '2381',
              '2382', '2383', '2384', '2385', '2386', '2387', '2388', '2389', '2390', '2391', '2392', '2393', '2394',
              '2395', '2396', '2397', '2398', '2399', '2401', '2402', '2403', '2404', '2405', '2406', '2407', '2408',
              '2409', '2410', '2411', '2412', '2413', '2414', '2415', '2416', '2417', '2418', '2419', '2420', '2421',
              '2422', '2423', '2424', '2425', '2426', '2427', '2428', '2429', '2430', '2431', '2432', '2433', '2434',
              '2435', '2436', '2437', '2438', '2439', '2440', '2441', '2442', '2443', '2444', '2445', '2446', '2447',
              '2448', '2449', '2450', '2451', '2452', '2453', '2454', '2455', '2456', '2457', '2458', '2459', '2460',
              '2461', '2462', '2463', '2464', '2465', '2466', '2467', '2468', '2469', '2470', '2471', '2472', '2473',
              '2474', '2475', '2476', '2477', '2478', '2479', '2480', '2481', '2482', '2483', '2484', '2485', '2486',
              '2487', '2488', '2489', '2490', '2491', '2492', '2493', '2494', '2495', '2496', '2497', '2498', '2499',
              '3001', '3002', '3003', '3004', '3005', '3006', '3007', '3008', '3009', '3010', '3011', '3012', '3013',
              '3014', '3015', '3016', '3017', '3018', '3019', '3020', '3021', '3022', '3023', '3024', '3025', '3026',
              '3027', '3028', '3029', '3030', '3031', '3032', '3033', '3034', '3035', '3036', '3037', '3038', '3039',
              '3040', '3041', '3042', '3043', '3044', '3045', '3046', '3047', '3048', '3049', '3050', '3051', '3052',
              '3053', '3054', '3055', '3056', '3057', '3058', '3059', '3060', '3061', '2501', '2504', '2505', '2506',
              '2509', '2511', '2512', '2514', '2515', '2516', '2520', '2521', '2523', '2524', '2525', '2526', '2527',
              '2528', '2530', '2533', '2534', '2535', '2536', '2537', '2538', '2539', '2540', '2542', '2543', '2544',
              '2545', '2546', '2547', '2548', '2601', '2603', '2604', '2605', '2606', '2607', '2608', '2609', '2610',
              '2611', '2612', '2613', '2614', '2615', '2616', '2617', '2618', '2701', '2702', '2704', '2705', '2706',
              '2707', '2854', '2855', '2856', '9101', '9102', '9801', '9902', '9904', '9905', '9906', '9907', '9908',
              '9910', '9911', '9912', '9914', '9915', '9917', '9918', '9919', '9921', '9922', '9924', '9925', '9926',
              '9927', '9928', '9929', '9930', '9931', '9933', '9934', '9935', '9936', '9937', '9938', '9939', '9940',
              '9941', '9942', '9943', '9944', '9945']

    def __init__(self):
        if not os.path.isdir(self.daily_path):
            os.mkdir(self.daily_path)
        last_get = sorted(os.listdir(self.daily_path))[-1][:4]
        self.start_index = self.stocks.index(last_get)

    def update_stocks(self):
        url = 'https://www.tej.com.tw/webtej/doc/uid.htm'
        q = requests.get(url)
        if q.status_code == 200:
            soup = BeautifulSoup(q.text, features='lxml')
            table = soup.find_all('table')[1]
            get_all = table.find_all(class_='xl24')
            new_stocks = [re.findall('>(\d+)<span', str(i))[0] for i in get_all if re.findall('>(\d+)<span', str(i))]
            new_stocks = [i for i in new_stocks if len(i) == 4]
            up_stocks = set(new_stocks) - set(self.stocks)
            down_stocks = set(self.stocks) - set(new_stocks)
            print(f'up: {up_stocks}, down: {down_stocks}')
            self.stocks = new_stocks
        print(f'connection error: {url}')

    def open_web(self):
        opts = Options()
        opts.add_argument("--incognito")
        ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        opts.add_argument("user-agent={}".format(ua))
        self.driver = webdriver.Chrome(self.py_path + '/chromedriver', chrome_options=opts)

        self.driver.get(self.stock_url)

    def get_stocks_data(self):
        if self.driver is None:
            print('first run open_web')
            return

        for check_stock_id in self.stocks[self.start_index + 1:]:
            if os.path.isfile(f'{self.daily_path}/{check_stock_id}.csv'):
                continue
            done = False
            while not done:
                if os.path.isfile(self.captcha_pic_path):
                    os.remove(self.captcha_pic_path)

                self.driver.refresh()
                self._enter_stock_id(check_stock_id)
                self._save_captcha_img()

                time.sleep(0.75)
                if not os.path.isfile(self.captcha_pic_path):
                    # maybe generate other web
                    self._close_other_web()
                    continue

                result = self._image_recognition_for_captcha()

                self._enter_captcha(result)

                if locateOnScreen(f'{self.pic_path}/error_pic_2.png'):
                    print('error! try more!')
                    continue

                if locateOnScreen(f'{self.pic_path}/no_data_pic.png'):
                    done = True
                    continue

                self._download_data()
                time.sleep(1)
                if not os.path.isfile(f'{self.download_path}/{check_stock_id}.csv'):
                    print('error! try more!')
                    continue
                done = True
                shutil.move(f'{self.download_path}/{check_stock_id}.csv',
                            f'{self.daily_path}/{check_stock_id}.csv')

    def get_alotof_captcha(self, times):
        for _ in range(times):
            self.driver.refresh()
            self._save_captcha_img()
            self._close_other_web()

    def _enter_stock_id(self, stock_id):
        pyautogui.click(x=217, y=303, duration=1)
        pyautogui.typewrite(stock_id)

    def _save_captcha_img(self):
        # click space -> right click -> download -> save
        pyautogui.click(x=179, y=344, duration=0.2)
        pyautogui.rightClick(x=174, y=396, duration=0.2)
        pyautogui.click(x=251, y=426, duration=0.2)
        pyautogui.sleep(0.5)
        pyautogui.press('enter')
        # pyautogui.click(x=737, y=313, duration=1)

    def _close_other_web(self):
        pyautogui.click(x=566, y=72)

    def _enter_captcha(self, captcha):
        pyautogui.click(x=231, y=441, duration=1)
        pyautogui.typewrite(captcha)
        pyautogui.press('enter')

    def _download_data(self):
        pyautogui.click(x=229, y=497, duration=0.5)

    def _image_recognition_for_captcha(self):
        target = cv2.imread(self.captcha_pic_path)
        kernel = np.ones((4, 4), np.uint8)
        erosion = cv2.erode(target, kernel, iterations=1)
        blurred = cv2.GaussianBlur(erosion, (5, 5), 0)
        edged = cv2.Canny(blurred, 30, 150)
        dilation = cv2.dilate(edged, kernel, iterations=1)
        result = pytesseract.image_to_string(dilation, config='stock').replace(' ', '')
        return result


if __name__ == '__main__':
    machine = GetDailyMachine()
    machine.open_web()
    machine.get_stocks_data()
