#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 15:21:50 2020

@author: robert.tseng
"""

# =============================================================================
# import lib 
# =============================================================================
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os 
import pytesseract
import time
# =============================================================================
# import desktop
# ============================================================================
def detect_img_str(image_dir):
    img =  cv2.imread(path+'/captcha_data/'+image_dir)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.imread(path+'LEPZK.png', 0)
    kernel = np.ones((4, 4), np.uint8)
    erosion = cv2.erode(gray_img, kernel, iterations=1)
    blurred = cv2.GaussianBlur(erosion, (5, 5), 0)
    edged = cv2.Canny(blurred, 30, 150)
    dilation = cv2.dilate(edged, kernel, iterations=1)
    cnts, _ = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boundingBoxes_area = [(cv2.boundingRect(c)[0],c) \
                          for c in cnts if cv2.contourArea(c) > 100]
    boundingBoxes_area = sorted(boundingBoxes_area, key = lambda x :x[0])[:5]
    # dilation_1 = cv2.cvtColor( dilation.copy(), cv2.COLOR_GRAY2RGB)
    ocr_str = []
    for _, c in boundingBoxes_area:
        x,y,w,h = cv2.boundingRect(c)
        sub_img = dilation[y:y+h, x:x+w]
        # sub_img = cv2.dilate(sub_img, kernel, iterations=1)
        sub_img = cv2.resize(sub_img, (50, 50))
        diff_data  = np.argmin(np.sum( np.sum((data.copy() - sub_img / 255)**2,\
                                axis = 2),axis = 1) )
        ocr_str.append(label[diff_data])
    ocr_str = ''.join(ocr_str)
    return ocr_str
        
if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(__file__))
    data = np.load( path + '/OCR/img.npy')
    label = np.load( path + '/OCR/label.npy')
    images_dir = os.listdir(path+'/captcha_data')
    correct = 0
    for image_dir in images_dir:
        ocr_str = detect_img_str(image_dir)
        if ocr_str == image_dir.split('.')[0]:
            correct += 1
        else:
            print(image_dir.split('.')[0], ocr_str)
    print(correct/len(images_dir))
    
     
