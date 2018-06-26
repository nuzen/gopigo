import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt 
import numpy as np
import cv2 as cv2
import gopigo3
#import pygame
import time
import easygopigo3 as easy
from pylab import *

# Simple threshold class that takes in a color image
# and generates a single threshold.

dexgp = gopigo3.GoPiGo3() # Creating driver class object, provided by dexter labs.
#my_buzzer = gopigo3.Buzzer("AD2", dexgp)

gpg = easy.EasyGoPiGo3()
my_distance_sensor = gpg.init_distance_sensor()
def fw(t):
    """
    Moves the robot forward for t seconds.
    """
    for i in range(0, int(t*100+1) ):
        dexgp.set_motor_power(dexgp.MOTOR_LEFT + dexgp.MOTOR_RIGHT, 100)
        time.sleep(0.01)
    #dexgp.reset_all()

def bw(t):
    """
    Moves the robot backward for t seconds.
    """
    for i in range(0, int(t*100+1)):
        dexgp.set_motor_power(dexgp.MOTOR_LEFT + dexgp.MOTOR_RIGHT, -100)
        time.sleep(0.01)
    #dexgp.reset_all()


def lt(degrees):
    dexgp.turn_degrees(-degrees)
    time.sleep(0.01)
    
    
def rt(degrees):
    dexgp.turn_degrees(degrees)
    time.sleep(0.01)

def tb():
    dexgp.turn_degrees(200)
    time.sleep(1)




class threshold:
    def __init__(self,color_img):        
        self.color_img     = color_img     # Color image to process           
        self.img           = np.array([])  # Component image
        self.threshold_img = np.array([])  # Thresholded image
        self.count_num = 0                    # Initial number of pixels
        self.index = 0                     # Color histogram index
        self.colors = ['Blue', 'Green', 'Red']      # Color strings
        self.th1   = -1                    # Invalid tresholds
        self.th2   = -1
        
        return

    # The @property  allows you to type
    #    object_name.original_img 
    # to access the member and you are still running the full function below.
    # We can add more checking code later to avoid mistakes.
    @property
    def original_img(self):
        return self.img
    
    @property
    def threshold_img_f(self):
        return self.threshold_img    
    
    # Returns the OpenCV color index
    def color_index(self,x):
        return {
            'red':2, 
            'RED':2, 
            'Red':2,
            'blue':0, 
            'BLUE':0, 
            'Blue':0,
            'green':1, 
            'GREEN':1, 
            'Green':1,
            }.get(x, 0)  # 0 is the default
                
    def sel_color_comp(self,color_string):
        self.index = self.color_index(color_string)
        self.img   = self.color_img[:,:,self.index]
        return            
       

################ WENJING SHI CHANGES
    def show_color_histograms(self):
        color = ('Blue','Green','Red')
        for i,col in enumerate(color):
            histr = cv2.calcHist([self.color_img],[i],None,[256],[0,256])
            plt.figure(color[i])
            plt.plot(histr,color = col)
            plt.xlabel('Pixel values')
            plt.ylabel('Number of occurrences')
            plt.title(color[i])
            plt.xlim([0,256])
            plt.title(col)
        plt.show()
        
    def show_color_histograms_img(self):
        color = ('Blue','Green','Red')
        for i,col in enumerate(color):
            histr = cv2.calcHist([self.color_img],[i],None,[256],[0,256])
            plt.figure(color[i])
            plt.plot(histr,color = col)
            plt.xlabel('Pixel values')
            plt.ylabel('Number of occurrences')
            plt.title(color[i])
            plt.xlim([0,256])
            plt.title(col)
            plt.savefig(col+'.png')
        
        blue = cv2.imread('Blue.png')
        green = cv2.imread('Green.png')
        red = cv2.imread('Red.png')
        rgb_hist = np.vstack((red, green, blue))
                         
        cv2.namedWindow('RGB Histograms',0)
        cv2.moveWindow('RGB Histograms', 1215,37)
        cv2.resizeWindow('RGB Histograms', 500,900)
        cv2.imshow('RGB Histograms', rgb_hist)
        #plt.show()


    def show_color_comb_hist(self):
        color = ('Blue','Green','Red')
        for i,col in enumerate(color):
            histr = cv2.calcHist([self.color_img],[i],None,[256],[0,256])
            plt.figure('RGB Histogram')
            plt.plot(histr,color = col)
            plt.xlabel('Pixel values')
            plt.ylabel('Number of occurrences')
            plt.title(color[i])
            plt.xlim([0,256])
            plt.title(col)
        plt.show()
        
        
    def show_hist_with_th(self, rgb_values):
        color = ('Blue','Green','Red')
        n = 0
        for i,col in enumerate(color):
            histr = cv2.calcHist([self.color_img],[i],None,[256],[0,256])
            plt.figure(color[i])
            plt.plot(histr,color = col)
            plt.axvline(x=rgb_values[n])
            plt.axvline(x=rgb_values[n+1])
            plt.xlabel('Pixel values', fontsize=18)
            plt.ylabel('Number of occurrences',fontsize=12)
            plt.title(color[i], fontsize = 18)
            plt.xlim([0,256])
            plt.title(col)
            plt.savefig(col+'.png')
            n=n+2
            plt.clf()
        
        blue = cv2.imread('Blue.png')
        green = cv2.imread('Green.png')
        red = cv2.imread('Red.png')
        rgb_hist = np.vstack((red, green, blue))
                         
        cv2.namedWindow('RGB Histograms',0)
        cv2.moveWindow('RGB Histograms', 1215,37)
        cv2.resizeWindow('RGB Histograms', 500,900)
        cv2.imshow('RGB Histograms', rgb_hist)
##########################################        
        
    def show_threshold(self,plot_name):
        histr = cv2.calcHist([self.color_img],[self.index],None,[256],[0,256])
        plt.figure()
        plt.plot(histr,color = self.colors[self.index])
        plt.xlim([0,256])
        plt.title(plot_name)
        
        ymax = self.color_img.shape[0] * self.color_img.shape[1] 
        if (self.th1>=0):
            plt.plot((self.th1,self.th1), (0,ymax), 'r-')
        if (self.th2>=0):
            plt.plot((self.th2,self.th2), (0,ymax), 'r-')        
        
        plt.show()
        
    def single_color(self, th, color_name):
##        print(th)
        if (color_name == 'r'):
            r=((self.color_img[:,:,2]/1.0*th/255)).astype(uint8)
            g=((self.color_img[:,:,1]/1.0*0)).astype(uint8)
            b=((self.color_img[:,:,0]/1.0*0)).astype(uint8)
        if (color_name == 'g'):
            r=((self.color_img[:,:,2]/1.0*0)).astype(uint8)
            g=((self.color_img[:,:,1]/1.0*th/255)).astype(uint8)
            b=((self.color_img[:,:,0]/1.0*0)).astype(uint8)
        if (color_name == 'b'):
            r=((self.color_img[:,:,2]/1.0*0)).astype(uint8)
            g=((self.color_img[:,:,1]/1.0*0)).astype(uint8)
            b=((self.color_img[:,:,0]/1.0*th/255)).astype(uint8)
                
        
        single_color_img = cv2.merge((b,g,r))               
        return single_color_img

    
##    def ThreshLow(self,HiVal):
##        #ret, th2_1 = cv2.threshold(self.img, 0, 255, cv2.THRESH_BINARY);
##        ret, th2 = cv2.threshold(self.img, HiVal, 255, cv2.THRESH_BINARY_INV)
##        self.threshold_img = th2
##        self.th1 = HiVal
##        self.th2 = -1
##        return self.threshold_img
##    
##    def ThreshHigh(self,LowVal):
##        ret, th1 = cv2.threshold(self.img, LowVal, 255, cv2.THRESH_BINARY);
####        ret, th1_1 = cv2.threshold(self.img, 255, 255, cv2.THRESH_BINARY_INV);
##        self.threshold_img = th1
##        self.th1 = LowVal
##        self.th2 = -1
##        return self.threshold_img

    def ThreshLow(self,LowVal):
        ret, th2_1 = cv2.threshold(self.img, 0, 255, cv2.THRESH_BINARY);
        ret, th2 = cv2.threshold(self.img, LowVal, 255, cv2.THRESH_BINARY_INV)
        self.threshold_img = th2&th2_1
        self.th1 = LowVal
        self.th2 = -1
        return self.threshold_img
    
    def ThreshHigh(self,HiVal):
        ret, th1 = cv2.threshold(self.img, HiVal, 255, cv2.THRESH_BINARY);
        ret, th1_1 = cv2.threshold(self.img, 255, 255, cv2.THRESH_BINARY_INV);
        self.threshold_img = th1&th1_1
        self.th1 = HiVal
        self.th2 = -1
        return self.threshold_img
    
    def ThreshRange(self,LowVal, HiVal):  
        ret, th3 = cv2.threshold(self.img, LowVal, 255, cv2.THRESH_BINARY);
        ret, th4 = cv2.threshold(self.img, HiVal, 255, cv2.THRESH_BINARY_INV);
        self.threshold_img = th3&th4
        self.th1 = LowVal
        self.th2 = HiVal
        return self.threshold_img
   
class thr_combination:
    def __init__(self, img, blueTh,greenTh,redTh):       
        row=img.shape[0]
        col=img.shape[1]
        
        allTh = (blueTh/255.0)*(greenTh/255.0)*(redTh/255.0)
        self.count = np.sum(allTh)        
        
        b=((img[:,:,0]/1.0)*allTh).astype(uint8)
        g=((img[:,:,1]/1.0)*allTh).astype(uint8)
        r=((img[:,:,2]/1.0)*allTh).astype(uint8)
                
        self.comb_img = cv2.merge((b,g,r))
        return 
        
    def im_show(self):
        #size_pct = 150 #  percentage of original size (e.g., 25, 50, 100)
        #self.comb_img = shrink_img(self.comb_img, size_pct)
        cv2.namedWindow('RGB Combination',0)
        cv2.moveWindow('RGB Combination', 515,600);
        cv2.imshow('RGB Combination', self.comb_img)
        cv2.resizeWindow('RGB Combination', 300,300)
        return 
    
    def return_result(self):
        return self.comb_img
                         
        
class comb_thr:
    def __init__(self, img, blueTh,greenTh,redTh,color_name, angle, action):
        self.centres = []
        self.areas = []
        self.action = action
        self.angle = angle
        self.color_name = color_name
        self.img = img
        self.center = []
        #row=img.shape[0]
        self.col=img.shape[1]
        self.comb_binary_img = (blueTh*greenTh*redTh).astype(np.uint8)
        
#        self.allTh = (blueTh/255.0)*(greenTh/255.0)*(redTh/255.0)
        _, self.contours, _ = cv2.findContours(self.comb_binary_img.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
#        self.count_num = np.sum(self.allTh)
#        b=((self.img[:,:,0]/1.0)*self.allTh).astype(np.uint8)
#        g=((self.img[:,:,1]/1.0)*self.allTh).astype(np.uint8)
#        r=((self.img[:,:,2]/1.0)*self.allTh).astype(np.uint8)
#                
#        self.comb_img = cv2.merge((b,g,r))
        self.markColorRegions()
                 
            
        if (self.action == 'test'):
            self.det_only()
        
        elif (self.action == 'det'):
            self.det_move()
            
        else:
            print ('Warning: Wrong action.')
            
        return
    

        
    ''' Only detect color regions '''
    def det_only(self):
        if (self.areas == []):
            return
        else:
            self.markLargest()
        
    ''' Detect color regions and move to the object '''
    def det_move(self):
        if (self.areas == []):
            #print('angle=', self.angle)
            self.searchTarget()

        # Mark the largest connected color part with a blue point
        else:
            self.searchLargest()
    
    
    
    ''' Find the largest color region and mark it with blue dot '''
    def markLargest(self):
        #all_areas = np.array(areas)
        max_area = max(self.areas)
        max_index = self.areas.index(max_area)
        cv2.circle(self.img, self.centres[max_index],2,(255,0,0),2)
        self.center = self.centres[max_index]
        
    ''' If robot cannot find any target, it will turn around by 360 degrees and then move
     forward for one second, until it finds color regions '''
    def searchTarget(self):
         if (self.angle == 360):
             self.checkDistance()
             #fw(1)
             time.sleep(0.1)
             print('Move forward for 1 sec')
             self.angle = 0
         else:
            rt(30)
            print('Turn right by 30 degrees')
            time.sleep(0.1)
            self.angle = self.angle+30
            
         return 
        
    ''' Make sure the largest color region (blue dot) is in the center range
    of the frame, if the dot in the left/right part of the image, the robot will
    turn left/right by 5 degrees, otherwise move forward '''
    def searchLargest(self):
        max_area = max(self.areas)
        max_index = self.areas.index(max_area)
        cv2.circle(self.img, self.centres[max_index],2,(255,0,0),2)
        # If the blue point at the left of the center, the robot
        # will turn left by 5 degrees.
        if (self.centres[max_index][0] < self.col/2-35 ):
            lt(5)
            print('Turn left')

                
            # If the blue point at the right of the center, the robot
            # will turn right by 5 degrees.
        elif (self.centres[max_index][0] > self.col/2+35 ):
            rt(5)
            print('Turn right')
                    
            # Otherwise move forward for one second
        else:
                    
            print('Move forward')
            self.findObj()
        
    ''' Mark all detected color regions with red dots '''
    def markColorRegions(self):
        # Find all color regions and mark them with red points       
        for i in range(len(self.contours)):
            cnt = self.contours[i]
            
            moments = cv2.moments(cnt)
            
            if (moments['m00'] != 0):
                self.centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
                cv2.circle(self.img, self.centres[-1],2,(0,0,255),-1)
                area = cv2.contourArea(cnt)
                
                self.areas.append(area)
                
        return
    
   
    
    ''' Display images from camera '''
    def im_show(self):
        
        cv2.imshow(self.color_name, self.img)
        cv2.waitKey(25)
        return (self.center, self.angle, self.img)

    def returnResults(self):
        if (self.areas == []):
            max_area= 0
        else:
            max_area = max(self.areas)
        return (self.center, self.angle, self.img, max_area)
            
    # The @property  allows you to type
    #    object_name.original_img 
    # to access the member and you are still running the full function below.
    # We can add more checking code later to avoid mistakes.
    @property
    def count(self):
        return self.count_pixels
    
    ''' After finding the object, move forward if the distance is larger than 
    250 mm. Otherwise the robot will dance to celebrate '''
    def findObj(self):
        if (my_distance_sensor.read_mm() > 250):
            fw(1)
            time.sleep(0.1)
        else:
            #print(my_distance_sensor.read_mm())
            self.dance()
            
    ''' Robot dances  '''
    def dance(self):
        for i in range (1, 4):
            bw(0.1)
            fw(0.1)
        
        bw(1)
        tb()
        fw(2)
        dexgp.reset_all()
     
    ''' Check the distance between the robot and the object'''    
    def checkDistance(self):
        if (my_distance_sensor.read_mm() < 250):
            tb()
            fw(1)
        else:
            fw(1)
        dexgp.reset_all()
            
        
            





                        
