# import time
#
# import pyautogui
#
# time.sleep(2)
# print(pyautogui.position())

import cv2
import os
import matplotlib.pyplot as plt
captcha_list = os.listdir('captcha_data')

target = cv2.imread(f'captcha_data/{captcha_list[0]}')
cv2.imshow('cool', target)