import AOLMERobots as gopi
import cv2

red_range   = [50, 255]
green_range = [0, 20]
blue_range  = [0, 20]

min_area = 5000
area = 0
while (area < min_area):
    img = gopi.get_image()
    x,y,area = gopi.get_img_object_center(img, red_range, green_range, blue_range)
    
    x0 = img.shape[0]/2
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
                
    cv2.imshow("Robot view", img)
    cv2.waitKey(10)
    print('Area = ', area)
    
    
cv2.destroyAllWindows()  