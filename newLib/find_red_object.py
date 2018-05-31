import AOLMERobots as gopi
import random
import pdb
#import cv2
#import gopigo3
from thresholds2 import threshold, comb_thr 
#dexgp = gopigo3.GoPiGo3()
# Resetting sensors
gopi.reset_sensors()

# Color thresholds
red_min_max = [50,255]
grn_min_max = [0,20]
blu_min_max = [0,50]

# Get image center
x0,y0       = gopi.get_image_center()


# Keep moving until it gets involved in collision
dist   = gopi.get_dist()

while(dist > 10):

    print("Object distance "+str(dist))
    
    # Get object center
    x,y,img     = gopi.get_object_center(red_min_max,
                                         grn_min_max,
                                         blu_min_max)
    # Updating object distance
    dist   = gopi.get_dist()
    
# Resetting sensors once the robot stops
gopi.reset_sensors()
