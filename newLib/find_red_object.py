import AOLMERobots as gopi
import random
from thresholds2 import threshold, comb_thr 

# Resetting all sensors
gopi.reset_sensors()

# Color thresholds
red_min_max = [50,255]
grn_min_max = [0,20]
blu_min_max = [0,50]

# Get image center, x is along widht, y is along height.
x0,y0       = gopi.get_image_center()


# Keep moving until it gets involved in collision
dist   = gopi.get_dist()

while(dist > 10):
    print("Distance to target",dist)
    
    # Get object center
    x,y,img     = gopi.get_object_center(red_min_max,
                                         grn_min_max,
                                         blu_min_max)
    # Show labelled image
    gopi.show_image(img)

    # Decide to turn right or left
    obj_dist = x - x0

    # Decide to move robot to left or right or forward
    
    if obj_dist >= 0:              # if (object is to right)
        print("Turning left")      # 
        if obj_dist > 100:         #   if (it is 100 pixels away from center)
            gopi.rt(0.5)           #        turn 0.5 seconds to right
        else:                      #   else
            gopi.fw(1)             #         move forward for 1 second

            
    else:                          # if (object to left)
        if obj_dist < -100:        #    if ( it is 100 pixels away from center)
            gopi.lt(0.5)           #         turn 0.5 seconds to left
        else:                      #    else
            gopi.fw(1)             #          move forward for 1 second

    # Updating object distance
    dist   = gopi.get_dist()
    
# Resetting sensors once the robot stops
gopi.reset_sensors()
