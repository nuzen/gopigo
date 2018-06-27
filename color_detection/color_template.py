import AOLMERobots as gopi
import cv2

# Setup the values to detect your range.
red_range   = [?, ?]   # Enter Red_min and Red_max
green_range = [?, ?]   # Enter Green_min and Green_max
blue_range  = [?, ?]   # Enter Blue_min and Blue_max

min_area = ?  # Enter minimum area
area = 0
while (area < min_area):
    img = gopi.get_image()
    x,y,area = gopi.get_img_object_center(img, red_range, green_range, blue_range)

    x0 = img.shape[0]/2  # Column center of the image.
    obj_dist = x - x0    # Deviation from the center

    # Decide how to move the robot:
    if obj_dist >= 0:
        if (obj_dist > ???):
            print("Robot is too far to the ?????")
            print("Robot needs to ????")
        else:
            print("Robot needs to ????")

    else:
        if (obj_dist < ???):
            print("Robot is too far to the ?????")
            print("Robot needs to ????")
        else:
            print("Robot needs to ????") 

    # Display the image from the Robot
    cv2.imshow("Robot view", img)
    cv2.waitKey(10)
    print('Area = ', area)


cv2.destroyAllWindows()
