"""
DESCRIPTION:
 This program implements color based object follower
 using aolme library.

ALGORITHM:
 Set thresholds for object color.
 Take picture
 Find picture center
 Find object center
 While (Inf)
   If (object center is empty list)
     Stop robot
   If (object coordinate along width is near center)
     Move robot forward for 1 second.
   If (object is to the right and not near center)
     Turn robot right for 10 degrees
   If (object is to the left and not near center)
     Turn robot left for 10 degrees
 
"""

import aolme
import cv2
# Initializing color thresholds and creating a single array
# having all the thresholds. ???How to explain what are doing here???!
RMin = 85    # Minimum value of red.
RMax = 255  # Maximum value of red.
GMin = 0    # Minimum value of Green.
GMax = 50  # Maximum value of Green.
BMin = 0    # Minimum value of Blue.
BMax = 50  # Maximum value of Blue.
MinMaxArray = [RMin, RMax, GMin, GMax, BMin, BMax] # Creating single array.

while True:
    img = aolme.getPic() # get picture from camera.

    # imgCent  = (x,y) => x = along width of the image
    #                  => y = along height of the image
    imgCent = aolme.getImgCenter(img) # get image center.
    objCent = aolme.getObjCenter(img, # get object center.
                                 MinMaxArray)

    if len(objCent) == 0:             # if the object is not
        break;                        # found, stop
    
    x_diff = objCent[0] - imgCent[0]
    if( abs(x_diff) <= 80 ):          # if the object close to
        aolme.fw(1)                   # center move for 1 second
        
    if (x_diff > 80):                 # if difference is positive
        aolme.rt(10)                  # the robot is to the right.
                                      # Turn right 10 degrees.
                                      
    if (x_diff < -80):                # if the difference is negative
        aolme.lt(10)                  # the robot is to the left.
                                      # Turn left 10 degrees.
