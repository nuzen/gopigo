# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 10:08:21 2018

@author: AOLME_2
"""

import AOLMERobots as gopi
import cv2

# Resetting all sensors
gopi.reset_sensors()

img = cv2.imread('ColorMap.png')
gopi.show_RGB_hist(img)