# import time
#
# import pyautogui
#
# time.sleep(2)
# print(pyautogui.position())

import cv2
import os
import pytesseract
import numpy as np
captcha_list = os.listdir('captcha_data')

r, w = 0, 0
for i in captcha_list:
    target = cv2.imread(f'captcha_data/{i}')
    kernel = np.ones((3, 3), np.uint8)

    erosion = cv2.erode(target, kernel, iterations=1)
    result = pytesseract.image_to_string(erosion, config='stock_1')
    if len(result) == 5:
        if result == i[:5]:
            r += 1
        else:
            w += 1
        continue
    blurred = cv2.GaussianBlur(erosion, (3, 3), 0)
    result = pytesseract.image_to_string(blurred, config='stock_1')
    if len(result) == 5:
        if result == i[:5]:
            r += 1
        else:
            w += 1
        continue
    edged = cv2.Canny(blurred, 50, 600)
    result = pytesseract.image_to_string(edged, config='stock_1')
    if len(result) == 5:
        if result == i[:5]:
            r += 1
        else:
            w += 1
        continue
    dilation = cv2.dilate(edged, kernel, iterations=1)
    result = pytesseract.image_to_string(dilation, config='stock_1')
    if result == i[:5]:
        r += 1
    else:
        w += 1
print(r, w)