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
image = gopi.get_image()

thr_obj = threshold(image)
cv2.namedWindow('image')

# Create sliders
def nothing(x):
    pass

cv2.createTrackbar('RL','image',0,255,nothing)
cv2.createTrackbar('RH','image',0,255,nothing)

cv2.createTrackbar('GL','image',0,255,nothing)
cv2.createTrackbar('GH','image',0,255,nothing)

cv2.createTrackbar('BL','image',0,255,nothing)
cv2.createTrackbar('BH','image',0,255,nothing)
switch = 'Quit'
cv2.createTrackbar(switch, 'image',1,1,nothing)


while(1):

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

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
    
    # Onlt show red channel of the image:
    RedLow_single = thr_obj.single_color(RedLow, 'r')
    RedRange_single = thr_obj.single_color(RedRange, 'r')
    RedHi_single = thr_obj.single_color(RedHi, 'r')
    
    # Green component processing:
    thr_obj.sel_color_comp ('green')
    GreenLow   =  thr_obj.ThreshLow   (greenLow)            
    GreenRange =  thr_obj.ThreshRange (greenLow , greenHi)   
    GreenHi    =  thr_obj.ThreshHigh  (greenHi)
    
    # Onlt show green channel of the image
    GreenLow_single = thr_obj.single_color(GreenLow, 'g')
    GreenRange_single = thr_obj.single_color(GreenRange, 'g')
    GreenHi_single = thr_obj.single_color(GreenHi, 'g')
    
    # Blue component processing:
    thr_obj.sel_color_comp ('blue')
    BlueLow   =  thr_obj.ThreshLow   (blueLow)            
    BlueRange =  thr_obj.ThreshRange (blueLow , blueHi)   
    BlueHi    =  thr_obj.ThreshHigh  (blueHi)             
   
    # Onlt show blue channel of the image
    BlueLow_single = thr_obj.single_color(BlueLow, 'b')
    BlueRange_single = thr_obj.single_color(BlueRange, 'b')
    BlueHi_single = thr_obj.single_color(BlueHi, 'b')
   
    # Generate the second window, including 9 single color images, one combination image, and text
    white= np.zeros((90, RedLow.shape[1], 3), np.uint8)
    white[:] = (255)

    vcat1 = cv2.vconcat((white, RedLow_single))
    vcat2 = cv2.vconcat((white, RedRange_single))
    vcat3 = cv2.vconcat((white, RedHi_single))
    
    vcat4 = cv2.vconcat((white, GreenLow_single))
    vcat5 = cv2.vconcat((white, GreenRange_single))
    vcat6 = cv2.vconcat((white, GreenHi_single))
    
    vcat7 = cv2.vconcat((white, BlueLow_single))
    vcat8 = cv2.vconcat((white, BlueRange_single))
    vcat9 = cv2.vconcat((white, BlueHi_single))
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(vcat1,'0<=v<RL',(30,50), font, 1.5,(0,0,0), 3, 0)
    cv2.putText(vcat2,'RL<=v<=RH',(30,50), font, 1.5,(0,0,0), 3, 0)
    cv2.putText(vcat3,'RH<v<=255',(30,50), font, 1.5,(0,0,0), 3, 0)
    cv2.putText(vcat4,'0<=v<GL',(30,50), font, 1.5,(0,0,0), 3, 0)
    cv2.putText(vcat5,'GL<=v<=GH',(30,50), font, 1.5,(0,0,0), 3, 0)
    cv2.putText(vcat6,'GH<v<=255',(30,50), font, 1.5,(0,0,0), 3, 0)
    cv2.putText(vcat7,'0<=v<BL',(30,50), font, 1.5,(0,0,0), 3, 0)
    cv2.putText(vcat8,'BL<=v<=BH',(30,50), font, 1.5,(0,0,0), 3, 0)
    cv2.putText(vcat9,'BH<v<=255',(30,50), font, 1.5,(0,0,0), 3, 0)
    
    red_all = np.hstack((vcat1, vcat2, vcat3))
    green_all = np.hstack((vcat4, vcat5, vcat6))
    blue_all = np.hstack((vcat7, vcat8, vcat9))
    
    rgb_all = np.vstack((red_all, green_all, blue_all))

    # Get middle-RGB combination
    comb_image = thr_combination(img, BlueRange,GreenRange, RedRange).return_result()   
    
    # Mark conter of color regions
    red_min_max = [redLow, redHi]
    grn_min_max = [greenLow, greenHi]
    blu_min_max = [blueLow, blueHi]
    
    x,y,det_img, max_area = gopi.get_img_object_center(img, red_min_max, grn_min_max, blu_min_max)
    white_2= np.zeros((90+RedLow.shape[0], 2*RedLow.shape[1], 3), np.uint8)
    white_2[:] = (255)    
    
    cv2.putText(white_2, str(redLow) +'<= Red <= '+str(redHi),(30,150), font, 1.5,(0,0,0), 3, 0)
    cv2.putText(white_2, str(greenLow)+ '<= Green <='+str(greenHi),(30,220), font, 1.5,(0,0,0), 3, 0)
    cv2.putText(white_2, str(blueLow) +'<= Blue <='+str(blueHi),(30, 290), font, 1.5,(0,0,0), 3, 0)
    cv2.putText(white_2,'LargestArea = '+str(int(max_area)),(30,360), font, 1.5,(0,0,0), 3, 0)
    
    plot_1 = np.vstack((white, comb_image))
    
    cv2.putText(plot_1,'Middle RGB Combination',(10,50), font, 1.2,(0,0,0), 3, 0)
    plot_2 = np.hstack((plot_1, white_2))
    plot_3 = np.vstack((rgb_all, plot_2))
    
    
    cv2.namedWindow('RGB binary',0)
    cv2.moveWindow('RGB binary', 515,37);
    cv2.imshow('RGB binary', plot_3)
    cv2.resizeWindow('RGB binary', 700,900)
    
    # Add the green dot for center of the image and display it
    cv2.circle(det_img, (int(image.shape[0]/2), int(image.shape[1]/2)),2,(0,255,0),2)
    cv2.imshow('image',det_img)
    
    cv2.waitKey(1000)
    
    # Show histograms for RGB color
    gopi.show_RGB_hist(img, rgb_values)    
    
    
cv2.destroyAllWindows()