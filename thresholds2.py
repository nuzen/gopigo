import matplotlib.pyplot as pyplot
import numpy as np
import cv2 as cv2
from matplotlib import pyplot as plt
import gopigo3
import pygame
import time
import easygopigo3 as easy

# Simple threshold class that takes in a color image
# and generates a single threshold.

dexgp = gopigo3.GoPiGo3() # Creating driver class object, provided by dexter labs.
my_buzzer = gopigo3.Buzzer("AD2", dexgp)

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

def turn_back():
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
       
                     
    def show_color_histograms(self):
        color = ('Blue','Green','Red')
        for i,col in enumerate(color):
            histr = cv2.calcHist([self.color_img],[i],None,[256],[0,256])
            plt.figure(color[i])
            plt.plot(histr,color = col)
            pyplot.xlabel('Pixel values')
            pyplot.ylabel('Number of occurrences')
            pyplot.title(color[i])
            plt.xlim([0,256])
            plt.title(col)
            plt.show()
    
    def show_threshold(self,plot_name):
        histr = cv2.calcHist([self.color_img],[self.index],None,[256],[0,256])
        plt.figure()
        plt.plot(histr,color = self.colors[self.index])
        plt.xlim([0,256])
        plt.title(plot_name)
        
        ymax = self.color_img.shape[0] * self.color_img.shape[1] 
        if (self.th1>=0):
            plt.plot((self.th1-2,self.th1), (0,ymax), 'r-')
        if (self.th2>=0):
            plt.plot((self.th2-2,self.th2), (0,ymax), 'r-')        
        
        plt.show()
        
        
    def ThreshHigh(self,LowVal,):
        ret, th1 = cv2.threshold(self.img, LowVal, 255, cv2.THRESH_BINARY);
        self.threshold_img = th1
        self.th1 = LowVal
        self.th2 = -1
        return th1

    def ThreshLow(self,HiVal):
        ret, th2 = cv2.threshold(self.img, HiVal, 255, cv2.THRESH_BINARY_INV);
        self.threshold_img = th2
        self.th1 = HiVal
        self.th2 = -1
        return th2
    
    def ThreshRange(self,LowVal, HiVal):
        ret, th3 = cv2.threshold(self.img, LowVal, 255, cv2.THRESH_BINARY);
        ret, th4 = cv2.threshold(self.img, HiVal, 255, cv2.THRESH_BINARY_INV);
        self.threshold_img = th3&th4
        self.th1 = LowVal
        self.th2 = HiVal
        return self.threshold_img
   
             
        
class comb_thr:
    def __init__(self, img, blueTh,greenTh,redTh,color_name,N, action):
        self.action = action
        self.N = N
        self.color_name = color_name
        self.img = img
        self.center = []
        row=img.shape[0]
        col=img.shape[1]
        
        allTh = (blueTh/255.0)*(greenTh/255.0)*(redTh/255.0)
       
        self.comb_binary_img = (blueTh*greenTh*redTh).astype(np.uint8)
        
        
        _, contours, _ = cv2.findContours(self.comb_binary_img.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
        
        #cv2.imshow('comb_binary_img', self.comb_binary_img)
        
        centres = []
        areas = []
      
        self.count_num = np.sum(allTh)
        
        b=((img[:,:,0]/1.0)*allTh).astype(np.uint8)
        g=((img[:,:,1]/1.0)*allTh).astype(np.uint8)
        r=((img[:,:,2]/1.0)*allTh).astype(np.uint8)
                
        self.comb_img = cv2.merge((b,g,r))
        

        # Find all color parts and mark them with red points       
        for i in range(len(contours)):
            cnt = contours[i]
            
            moments = cv2.moments(cnt)
            
            if (moments['m00'] != 0):
                centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
                cv2.circle(self.img, centres[-1],2,(0,0,255),-1)
                area = cv2.contourArea(cnt)
                
                areas.append(area)
                
        if (self.action == 'det'):

            # If robot cannot find any target, it will turn around and then move
            # forward for one second, until it gets color.
            
            if (areas == []):
                #print('N=', self.N)
                if (self.N%(22) ==0):
                    self.check_distance()
                    #fw(1)
                    time.sleep(0.1)
                    print('Move forward for 1 sec')
                    self.N = self.N+1
                else:
                    rt(30)
                    print('Turn right by 30 degrees')
                    time.sleep(0.1)
                    self.N = self.N+1
            
                return 

            # Mark the largest connected color part with a blue point
            else:
                max_area = max(areas)
                max_index = areas.index(max_area)
                cv2.circle(self.img, centres[max_index],2,(255,0,0),2)
                # If the blue point at the left of the center, the robot
                # will turn left by 5 degrees.
                if (centres[max_index][0] < col/2-35 ):
                    lt(5)
                    print('Turn left')

                
                # If the blue point at the right of the center, the robot
                # will turn right by 5 degrees.
                elif (centres[max_index][0] > col/2+35 ):
                    rt(5)
                    print('Turn right')
                    
                # Otherwise move forward for one second
                else:
                    
                    print('Move forward')
                    self.find_obj()

        elif (self.action == 'test'):
            if (areas == []):
                return
            else:
                #all_areas = np.array(areas)
                max_area = max(areas)
                max_index = areas.index(max_area)
                cv2.circle(self.img, centres[max_index],2,(255,0,0),2)
                self.center = centres[max_index]
        else:
            print ('Warning: Wrong action.')
            
       
        return

    def im_show(self):
        
        cv2.imshow(self.color_name, self.img)
        
        
        return (self.center, self.N, self.img)

    def returnResults(self):
        return (self.center, self.N, self.img)
            
    # The @property  allows you to type
    #    object_name.original_img 
    # to access the member and you are still running the full function below.
    # We can add more checking code later to avoid mistakes.
    @property
    def count(self):
        return self.count_pixels

    def find_obj(self):
        if (my_distance_sensor.read_mm() > 250):
            fw(1)
            time.sleep(0.1)
        if (my_distance_sensor.read_mm() < 250):
            #print(my_distance_sensor.read_mm())
            bw(0.1)
            fw(0.1)
            bw(0.1)
            fw(0.1)
            bw(0.1)
            fw(0.1)
            bw(0.1)
            fw(0.1)
            bw(1)
            turn_back()
            fw(2)
            dexgp.reset_all()

    def check_distance(self):
        if (my_distance_sensor.read_mm() < 250):
            turn_back()
            fw(1)
        else:
            fw(1)
        dexgp.reset_all()
            
        
            





                        
