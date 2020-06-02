import datetime
import os
import shutil
import time

import cv2
import numpy as np
import pytesseract
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# setting
class GetDailyMachine:
    stock_url = 'https://bsr.twse.com.tw/bshtm/bsMenu.aspx'
    py_path = os.path.abspath(os.path.dirname(__file__))
    download_path = '/Users/yushi.chen/Downloads'
    captcha_pic_path = f'{download_path}/CaptchaImage.jpeg'
    today = str(datetime.date.today())
    daily_path = f'{py_path}/daily/{today}'
    pic_path = py_path + '/pic'

    driver = None
    stocks = ['1101', '1102', '1103', '1104', '1108', '1109', '1110', '1201', '1203', '1210', '1213', '1215', '1216',
              '1217', '1218', '1219', '1220', '1225', '1227', '1229', '1231', '1232', '1233', '1234', '1235', '1236',
              '1256', '1301', '1303', '1304', '1305', '1307', '1308', '1309', '1310', '1312', '1313', '1314', '1315',
              '1316', '1319', '1321', '1323', '1324', '1325', '1326', '1337', '1338', '1339', '1340', '1341', '1402',
              '1409', '1410', '1413', '1414', '1416', '1417', '1418', '1419', '1423', '1432', '1434', '1435', '1436',
              '1437', '1438', '1439', '1440', '1441', '1442', '1443', '1444', '1445', '1446', '1447', '1449', '1451',
              '1452', '1453', '1454', '1455', '1456', '1457', '1459', '1460', '1463', '1464', '1465', '1466', '1467',
              '1468', '1470', '1471', '1472', '1473', '1474', '1475', '1476', '1477', '1503', '1504', '1506', '1507',
              '1512', '1513', '1514', '1515', '1516', '1517', '1519', '1521', '1522', '1524', '1525', '1526', '1527',
              '1528', '1529', '1530', '1531', '1532', '1533', '1535', '1536', '1537', '1538', '1539', '1540', '1541',
              '1558', '1560', '1568', '1582', '1583', '1587', '1589', '1590', '1592', '1598', '1603', '1604', '1605',
              '1608', '1609', '1611', '1612', '1614', '1615', '1616', '1617', '1618', '1626', '1701', '1702', '1707',
              '1708', '1709', '1710', '1711', '1712', '1713', '1714', '1717', '1718', '1720', '1721', '1722', '1723',
              '1724', '1725', '1726', '1727', '1730', '1731', '1732', '1733', '1734', '1735', '1736', '1737', '1760',
              '1762', '1773', '1776', '1783', '1786', '1789', '1795', '1802', '1805', '1806', '1808', '1809', '1810',
              '1817', '1903', '1904', '1905', '1906', '1907', '1909', '2002', '2006', '2007', '2008', '2009', '2010',
              '2012', '2013', '2014', '2015', '2017', '2020', '2022', '2023', '2024', '2025', '2027', '2028', '2029',
              '2030', '2031', '2032', '2033', '2034', '2038', '2049', '2059', '2062', '2069', '2101', '2102', '2103',
              '2104', '2105', '2106', '2107', '2108', '2109', '2114', '2115', '2201', '2204', '2206', '2207', '2208',
              '2227', '2228', '2231', '2233', '2236', '2239', '2243', '2301', '2302', '2303', '2305', '2308', '2312',
              '2313', '2314', '2316', '2317', '2321', '2323', '2324', '2327', '2328', '2329', '2330', '2331', '2332',
              '2337', '2338', '2340', '2342', '2344', '2345', '2347', '2348', '2349', '2351', '2352', '2353', '2354',
              '2355', '2356', '2357', '2358', '2359', '2360', '2362', '2363', '2364', '2365', '2367', '2368', '2369',
              '2371', '2373', '2374', '2375', '2376', '2377', '2379', '2380', '2382', '2383', '2385', '2387', '2388',
              '2390', '2392', '2393', '2395', '2397', '2399', '2401', '2402', '2404', '2405', '2406', '2408', '2409',
              '2412', '2413', '2414', '2415', '2417', '2419', '2420', '2421', '2423', '2424', '2425', '2426', '2427',
              '2428', '2429', '2430', '2431', '2433', '2434', '2436', '2438', '2439', '2440', '2441', '2442', '2443',
              '2444', '2448', '2449', '2450', '2451', '2453', '2454', '2455', '2456', '2457', '2458', '2459', '2460',
              '2461', '2462', '2464', '2465', '2466', '2467', '2468', '2471', '2472', '2474', '2476', '2477', '2478',
              '2480', '2481', '2482', '2483', '2484', '2485', '2486', '2488', '2489', '2491', '2492', '2493', '2495',
              '2496', '2497', '2498', '2499', '2501', '2504', '2505', '2506', '2509', '2511', '2514', '2515', '2516',
              '2520', '2524', '2527', '2528', '2530', '2534', '2535', '2536', '2537', '2538', '2539', '2540', '2542',
              '2543', '2545', '2546', '2547', '2548', '2597', '2601', '2603', '2605', '2606', '2607', '2608', '2609',
              '2610', '2611', '2612', '2613', '2614', '2615', '2616', '2617', '2618', '2630', '2633', '2634', '2636',
              '2637', '2642', '2701', '2702', '2704', '2705', '2706', '2707', '2712', '2722', '2723', '2727', '2731',
              '2739', '2748', '2801', '2809', '2812', '2816', '2820', '2823', '2832', '2834', '2836', '2838', '2841',
              '2845', '2849', '2850', '2851', '2852', '2855', '2867', '2880', '2881', '2882', '2883', '2884', '2885',
              '2886', '2887', '2888', '2889', '2890', '2891', '2892', '2897', '2901', '2903', '2904', '2905', '2906',
              '2908', '2910', '2911', '2912', '2913', '2915', '2923', '2929', '2936', '2939', '3002', '3003', '3004',
              '3005', '3006', '3008', '3010', '3011', '3013', '3014', '3015', '3016', '3017', '3018', '3019', '3021',
              '3022', '3023', '3024', '3025', '3026', '3027', '3028', '3029', '3030', '3031', '3032', '3033', '3034',
              '3035', '3036', '3037', '3038', '3040', '3041', '3042', '3043', '3044', '3045', '3046', '3047', '3048',
              '3049', '3050', '3051', '3052', '3054', '3055', '3056', '3057', '3058', '3059', '3060', '3062', '3090',
              '3094', '3130', '3149', '3164', '3167', '3189', '3209', '3229', '3231', '3257', '3266', '3296', '3305',
              '3308', '3311', '3312', '3321', '3338', '3346', '3356', '3376', '3380', '3383', '3406', '3413', '3416',
              '3419', '3432', '3437', '3443', '3450', '3454', '3481', '3494', '3501', '3504', '3515', '3518', '3528',
              '3530', '3532', '3533', '3535', '3536', '3543', '3545', '3550', '3557', '3563', '3576', '3583', '3588',
              '3591', '3593', '3596', '3605', '3607', '3617', '3622', '3645', '3653', '3661', '3665', '3669', '3673',
              '3679', '3682', '3686', '3694', '3698', '3701', '3702', '3703', '3704', '3705', '3706', '3708', '3711',
              '3712', '4104', '4106', '4108', '4119', '4133', '4137', '4141', '4142', '4144', '4155', '4164', '4190',
              '4306', '4414', '4426', '4438', '4439', '4526', '4532', '4536', '4540', '4545', '4551', '4552', '4555',
              '4557', '4560', '4562', '4564', '4566', '4571', '4572', '4576', '4581', '4720', '4722', '4725', '4737',
              '4739', '4746', '4755', '4763', '4764', '4766', '4807', '4904', '4906', '4912', '4915', '4916', '4919',
              '4927', '4930', '4934', '4935', '4938', '4942', '4943', '4952', '4956', '4958', '4960', '4961', '4967',
              '4968', '4976', '4977', '4989', '4994', '4999', '5007', '5203', '5215', '5225', '5234', '5243', '5258',
              '5264', '5269', '5283', '5284', '5285', '5288', '5305', '5388', '5434', '5469', '5471', '5484', '5515',
              '5519', '5521', '5522', '5525', '5531', '5533', '5534', '5538', '5546', '5607', '5608', '5706', '5871',
              '5876', '5880', '5906', '5907', '6005', '6024', '6108', '6112', '6115', '6116', '6117', '6120', '6128',
              '6131', '6133', '6136', '6139', '6141', '6142', '6152', '6153', '6155', '6164', '6165', '6166', '6168',
              '6172', '6176', '6177', '6183', '6184', '6189', '6191', '6192', '6196', '6197', '6201', '6202', '6205',
              '6206', '6209', '6213', '6214', '6215', '6216', '6224', '6225', '6226', '6230', '6235', '6239', '6243',
              '6251', '6257', '6269', '6271', '6277', '6278', '6281', '6282', '6283', '6285', '6288', '6289', '6405',
              '6409', '6412', '6414', '6415', '6416', '6431', '6442', '6443', '6449', '6451', '6452', '6456', '6464',
              '6477', '6491', '6504', '6505', '6525', '6531', '6533', '6541', '6552', '6558', '6573', '6579', '6581',
              '6582', '6591', '6592', '6605', '6625', '6641', '6655', '6666', '6668', '6669', '6670', '6671', '6672',
              '6674', '6698', '6706', '6715', '8011', '8016', '8021', '8028', '8033', '8039', '8046', '8070', '8072',
              '8081', '8101', '8103', '8104', '8105', '8110', '8112', '8114', '8131', '8150', '8163', '8201', '8210',
              '8213', '8215', '8222', '8249', '8261', '8271', '8341', '8367', '8374', '8404', '8411', '8422', '8427',
              '8429', '8442', '8443', '8454', '8462', '8463', '8464', '8466', '8467', '8473', '8478', '8480', '8481',
              '8482', '8488', '8497', '8499', '8926', '8940', '8996', '9802', '9902', '9904', '9905', '9906', '9907',
              '9908', '9910', '9911', '9912', '9914', '9917', '9918', '9919', '9921', '9924', '9925', '9926', '9927',
              '9928', '9929', '9930', '9931', '9933', '9934', '9935', '9937', '9938', '9939', '9940', '9941', '9942',
              '9943', '9944', '9945', '9946', '9955', '9958', '0050', '0051', '0052', '0053', '0054', '0055', '0056',
              '0057', '0061', '9103', '9105', '9110', '9136', '9188']

    def __init__(self):
        self.check_add_folder(f'{self.py_path}/daily')
        self.check_add_folder(self.daily_path)
        if os.listdir(self.daily_path):
            for i in os.listdir(self.daily_path):
                self.stocks.remove(i[:4])
        self.stocks += ['excd']

    def check_add_folder(self, f_path):
        if not os.path.isdir(f_path):
            os.mkdir(f_path)

    def update_stocks(self):
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
            self.stocks = [i for i in stock if len(i) == 4]

    def open_web(self):
        opts = Options()
        opts.add_argument("--headless")
        # opts.add_argument("--incognito")
        ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        opts.add_argument("user-agent={}".format(ua))
        self.driver = webdriver.Chrome(self.py_path + '/chromedriver', chrome_options=opts)

        self.driver.get(self.stock_url)

    def get_stocks_data(self):
        if self.driver is None:
            print('first run open_web')
            return

        for check_stock_id in self.stocks:
            done = False
            while not done:
                if os.path.isfile(f'{self.py_path}/{check_stock_id}.csv'):
                    done = True
                    continue
                self._init_action()

                result = self._some_action(check_stock_id)

                while self._error_msg('驗證碼'):
                    shutil.move(self.captcha_pic_path,
                                f'{self.py_path}/captcha_data/error/{result}.png')
                    print(f'captcha error! {result}')
                    result = self._some_action(check_stock_id)
                    time.sleep(0.2)

                if self._error_msg('查無資'):
                    done = True
                    continue

                self._download_data()
                time.sleep(0.5)
                print(f'download csv: {check_stock_id}')
                shutil.move(self.captcha_pic_path,
                            f'{self.py_path}/captcha_data/{result}.png')
                done = True

        for check_stock_id in self.stocks:
            shutil.move(f'{self.py_path}/{check_stock_id}.csv',
                        f'{self.daily_path}/{check_stock_id}.csv')

    def _init_action(self):
        if os.path.isfile(self.captcha_pic_path):
            os.remove(self.captcha_pic_path)

    def _some_action(self, stock_id):
        if stock_id == 'excd':
            self._click_excd_deal()
        else:
            self._enter_stock_id(stock_id)
        self._save_captcha_img()
        result = self._image_recognition_for_captcha()
        self._enter_captcha(result)
        time.sleep(0.2)
        return result

    def _enter_stock_id(self, stock_id):
        self.driver.find_element_by_xpath("//input[@id='RadioButton_Normal']").click()
        stkno = self.driver.find_element_by_xpath("//input[@id='TextBox_Stkno']")
        stkno.clear()
        stkno.send_keys(stock_id)

    def _click_excd_deal(self):
        self.driver.find_element_by_xpath("//input[@id='RadioButton_Excd']").click()

    def _save_captcha_img(self):
        captcha_location = self.driver.find_element_by_xpath(
            "//div[@id='Panel_bshtm']//table//tbody//tr//td//table//tbody//tr//td//div//div//img")
        with open(self.captcha_pic_path, 'wb') as file:
            file.write(captcha_location.screenshot_as_png)

    def _reset_captcha(self):
        self.driver.find_element_by_xpath("//input[@id='Button_Reset']").click()

    def _enter_captcha(self, captcha):
        self.driver.find_element_by_xpath("//input[@name='CaptchaControl1']").send_keys(captcha)
        self.driver.find_element_by_xpath("//input[@id='btnOK']").click()

    def _download_data(self):
        self.driver.find_element_by_xpath("//a[@id='HyperLink_DownloadCSV']").click()

    def _error_msg(self, str):
        return self.driver.find_element_by_xpath("//span[@id='Label_ErrorMsg']").text[:3] == str

    def _image_recognition_for_captcha(self):
        if os.path.isfile(self.captcha_pic_path):
            target = cv2.imread(self.captcha_pic_path)
            kernel = np.ones((3, 3), np.uint8)
            erosion = cv2.erode(target, kernel, iterations=1)
            result = pytesseract.image_to_string(erosion, config='stock_1').replace(' ', '')
            if len(result) == 5:
                cv2.destroyAllWindows()
                return result
            blurred = cv2.GaussianBlur(erosion, (3, 3), 0)
            result = pytesseract.image_to_string(blurred, config='stock_1').replace(' ', '')
            if len(result) == 5:
                cv2.destroyAllWindows()
                return result
            edged = cv2.Canny(blurred, 50, 600)
            result = pytesseract.image_to_string(edged, config='stock_1').replace(' ', '')
            if len(result) == 5:
                cv2.destroyAllWindows()
                return result
            dilation = cv2.dilate(edged, kernel, iterations=1)
            result = pytesseract.image_to_string(dilation, config='stock_1').replace(' ', '')
            cv2.destroyAllWindows()
        else:
            result = ''
        return result


if __name__ == '__main__':
    machine = GetDailyMachine()
    machine.open_web()
    while True:
        try:
            machine.get_stocks_data()
        except Exception as e:
            print(f'error {e}')