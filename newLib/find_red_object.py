import AOLMERobots as gopi
import random
import pdb

# Resetting sensors
gopi.reset_sensors()

# Color thresholds
red_min_max = [0,255]
grn_min_max = [0,255]
blu_min_max = [0,255]

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
    # Show object
    gopi.show_image(img)

    # ??? Should work on logic on how to move robot.
    # for now I am randomly moving robot fw and rt
    a = random.uniform(0,1)
    if a == 0:
        gopi.fw(1)
    else:
        gopi.rt(0.5)

    # Updating object distance
    dist   = gopi.get_dist()

# Resetting sensors once the robot stops
gopi.reset_sensors()
    
        
