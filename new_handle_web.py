import datetime
import json
import os
import shutil
import time
from collections import deque

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
    download_path = '/Users/csro/Downloads'
    captcha_pic_path = f'{download_path}/CaptchaImage.jpeg'
    today = str(datetime.date.today())
    daily_path = f'{py_path}/daily/{today}'
    pic_path = py_path + '/pic'

    driver = None

    def __init__(self):
        self.check_add_folder(f'{self.py_path}/daily')
        self.check_add_folder(self.daily_path)
        self.download_done, self.no_data = deque(), deque()

        with open('stock_list.json', 'r') as fp:
            self.stocks = json.load(fp)

        self.stocks += ['excd']

        for i in os.listdir(self.daily_path):
            self.stocks.remove(i[:4])

        self.start_time = time.time()
        self.get_number = len(self.stocks)

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
                    context = all_data[0].split('\u3000')[0]
                    if len(context) == 4:
                        stock.append(context)
            json_stock = json.dumps(stock)
            with open(f'{self.py_path}/stock_list.json', 'w') as fp:
                fp.write(json_stock)

    def open_web(self):
        opts = Options()
        opts.add_argument("--headless")
        # opts.add_argument("--incognito")
        ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        opts.add_argument("user-agent={}".format(ua))
        self.driver = webdriver.Chrome(self.py_path + '/chromedriver', chrome_options=opts)

        self.driver.get(self.stock_url)

    def get_stocks_data(self, save_captcha=False):
        if self.driver is None:
            print('first run open_web')
            return

        for i in self.download_done:
            if i in self.stocks:
                self.stocks.remove(i)
        for i in self.no_data:
            if i in self.stocks:
                self.stocks.remove(i)

        for check_stock_id in self.stocks:
            done = False
            while not done:
                if os.path.isfile(f'{self.py_path}/{check_stock_id}.csv') or os.path.isfile(
                        f'{self.daily_path}/{check_stock_id}.csv'):
                    done = True
                    continue
                self._init_action()

                result = self._some_action(check_stock_id)

                while self._error_msg('驗證碼'):
                    if save_captcha:
                        shutil.move(self.captcha_pic_path,
                                    f'{self.py_path}/captcha_data/error/{result}.png')
                    # print(f'captcha error! {result}')
                    result = self._some_action(check_stock_id)

                if self._error_msg('查無資'):
                    self.no_data.append(check_stock_id)
                    done = True
                    self._print_cost_time(check_stock_id, 'no data')
                    continue

                self._download_data()
                self.download_done.append(check_stock_id)

                self._print_cost_time(check_stock_id, 'download')

                if save_captcha:
                    shutil.move(self.captcha_pic_path,
                                f'{self.py_path}/captcha_data/{result}.png')
                done = True
        print(f'need to move: {self.download_done}')
        for check_stock_id in self.download_done:
            shutil.move(f'{self.py_path}/{check_stock_id}.csv',
                        f'{self.daily_path}/{check_stock_id}.csv')
        print('done!!!!')

    def _print_cost_time(self, stock_id, done_type):
        done_number = len(self.download_done) + len(self.no_data)
        cur_time = time.time()
        avg_time = (cur_time - self.start_time) / done_number

        print(
            f'stock: {stock_id}, '
            f'done type: {done_type}, '
            f'current done: {done_number}/{self.get_number}, '
            f'avg. time: {round(avg_time, 4)}, '
            f'estimate total time: {round(self.get_number * avg_time, 4)}, '
            f'current cost time: {round(cur_time - self.start_time, 4)}')

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
