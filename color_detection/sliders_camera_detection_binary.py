# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 10:00:44 2018

@author: AOLME_2
"""

import AOLMERobots as gopi
from thresholds2 import *
import cv2
# Resetting all sensors
gopi.reset_sensors()

cv2.namedWindow('image')
cv2.moveWindow('image', 10,37)
image = gopi.get_image()
cv2.imshow('image',image)
cv2.waitKey(10)

init_RL = input('Initial RedLow = ')
init_RH = input('Initial RedHi = ')
init_GL = input('Initial GreenLow = ')
init_GH = input('Initial GreenHi = ')
init_BL = input('Initial BlueLow = ')
init_BH = input('Initial BlueHi = ')
region = input('Largest detected region size (such as 50000) = ')
distance = input('Shortest detected region distance (such as 100) = ')

# Create sliders
def nothing(x):
    pass

cv2.createTrackbar('RL','image',int(init_RL),255,nothing)
cv2.createTrackbar('RH','image',int(init_RH),255,nothing)

cv2.createTrackbar('GL','image',int(init_GL),255,nothing)
cv2.createTrackbar('GH','image',int(init_GH),255,nothing)

cv2.createTrackbar('BL','image',int(init_BL),255,nothing)
cv2.createTrackbar('BH','image',int(init_BH),255,nothing)
switch = 'Quit'
cv2.createTrackbar(switch, 'image',1,1,nothing)


while(1):

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    image = gopi.get_image()
    thr_obj = threshold(image)
    img = image.copy()
    
    # get current positions of six trackbars
    redLow = cv2.getTrackbarPos('RL','image')
    redHi = cv2.getTrackbarPos('RH','image')
    
    greenLow = cv2.getTrackbarPos('GL','image')
    greenHi = cv2.getTrackbarPos('GH','image')
    
    blueLow = cv2.getTrackbarPos('BL','image')
    blueHi = cv2.getTrackbarPos('BH','image')
    s = cv2.getTrackbarPos(switch,'image')
    if s == 0:
        break
    rgb_values = [blueLow, blueHi, greenLow, greenHi, redLow, redHi]
    
    # Red component processing:
    thr_obj.sel_color_comp ('red')
    RedLow   =  thr_obj.ThreshLow   (redLow)            
    RedRange =  thr_obj.ThreshRange (redLow , redHi)   
    RedHi    =  thr_obj.ThreshHigh  (redHi)
    
    # Green component processing:
    thr_obj.sel_color_comp ('green')
    GreenLow   =  thr_obj.ThreshLow   (greenLow)            
    GreenRange =  thr_obj.ThreshRange (greenLow , greenHi)   
    GreenHi    =  thr_obj.ThreshHigh  (greenHi)
        
    # Blue component processing:
    thr_obj.sel_color_comp ('blue')
    BlueLow   =  thr_obj.ThreshLow   (blueLow)            
    BlueRange =  thr_obj.ThreshRange (blueLow , blueHi)   
    BlueHi    =  thr_obj.ThreshHigh  (blueHi)             
   
    comb_image, comb_allTh= thr_combination(img, BlueRange,GreenRange, RedRange).return_result()   
    
    # Mark conter of color regions
    red_min_max = [redLow, redHi]
    grn_min_max = [greenLow, greenHi]
    blu_min_max = [blueLow, blueHi]
    
    x,y,det_img, max_area = gopi.get_img_object_center(img, red_min_max, grn_min_max, blu_min_max)
    
    # Add the green dot for center of the image and display it
    cv2.circle(det_img, (int(image.shape[0]/2), int(image.shape[1]/2)),2,(0,255,0),2)
    cv2.imshow('image',det_img)
    
    dist   = gopi.get_dist()
    print('Distance = ', dist)
    print('Largest Area = ', max_area)
    
    x0 = int(image.shape[1]/2)
    if (max_area>int(region)) | (dist<int(distance)):
        gopi.bw(1)
        gopi.rt(1)
    else:
        obj_dist = x - x0

        # Decide to move robot to left or right or forward
    
        if obj_dist >= 0:              # if (object is to right)
            print("Turning left")      # 
            if obj_dist > 100:         #   if (it is 100 pixels away from center)
                gopi.rt(0.2)           #        turn 0.5 seconds to right
            else:                      #   else
                gopi.fw(1)             #         move forward for 1 second

            
        else:                          # if (object to left)
            if obj_dist < -100:        #    if ( it is 100 pixels away from center)
                gopi.lt(0.2)           #         turn 0.5 seconds to left
            else:                      #    else
                gopi.fw(1)  
    cv2.waitKey(10)
    
    
    
cv2.destroyAllWindows()



