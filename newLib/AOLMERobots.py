# Gopigo modules
import gopigo3
import easygopigo3 as easy
# Raspberry pi camera modules
from picamera.array import PiRGBArray
from picamera import PiCamera
# Python modules
import time
import cv2
import math
import pdb
import random
# Wenjing image threshold module
from thresholds2 import threshold, comb_thr

DEBUG=True


def help_all():
    """
    Provides a list of all of the functions and classes
    in the module.
    """
    list_funs = """
                MOVEMENT
    fw(t): Move  forward  for t seconds.
    bw(t): Move  backward for t seconds.
    rt(t): Turns right    for t seconds.
    lt(t): Turns left     for t seconds.
    rtd(d): Turns right for d degrees.
    ltd(d): Turns left for d degrees.
    To see example, type:
      import AOLMERobots as gopi
      help(gopi.fw)

                DISTANCE Sensor
    get_dist(): Gives you obstacle distance.

                Sensor controls
    reset_sensors():  Resets all sensors.
    """
    print(list_funs)


"""
                Movement
"""
def fw(t):
    """
    Moves forward for t seconds.
    
    Example:
    import AOLMERobots as gopi
    gopi.fw(3)
    """
    if DEBUG:
        print("\tMoving forward for",t,"sec")
    dexgp = gopigo3.GoPiGo3()
    for i in range(0, int(t*100+1)):
        dexgp.set_motor_power(dexgp.MOTOR_LEFT + dexgp.MOTOR_RIGHT, 100)
        time.sleep(0.01)
    dexgp.set_motor_power(dexgp.MOTOR_LEFT + dexgp.MOTOR_RIGHT, 0)

    
def bw(t):
    """
    Moves backward for t seconds.
    
    Example:
    import AOLMERobots as gopi
    gopi.bw(3)
    """
    if DEBUG:
        print("\tMoving backward for",t,"sec")
    dexgp = gopigo3.GoPiGo3()
    for i in range(0, int(t*100+1)):
        dexgp.set_motor_power(dexgp.MOTOR_LEFT + dexgp.MOTOR_RIGHT, -100)
        time.sleep(0.01)
    dexgp.set_motor_power(dexgp.MOTOR_LEFT + dexgp.MOTOR_RIGHT, 0)

    
def rt(t):
    """
    Turns right for t seconds.

    Example:
    import AOLMERobots as gopi
    gopi.rt(1)
    """
    if DEBUG:
        print("\tTurning right for",t,"sec")
    dexgp = gopigo3.GoPiGo3()
    for i in range(0, int(t*100+1)):
        dexgp.set_motor_power(dexgp.MOTOR_LEFT, 100)
        dexgp.set_motor_power(dexgp.MOTOR_RIGHT,0)
        time.sleep(0.01)
    dexgp.set_motor_power(dexgp.MOTOR_LEFT + dexgp.MOTOR_RIGHT, 0)

    

def lt(t):
    """
    Turns left for t seconds.

    Example:
    import AOLMERobots as gopi
    gopi.lt(1)
    """
    if DEBUG:
        print("\tTurning left for",t,"sec")
    dexgp = gopigo3.GoPiGo3()
    for i in range(0, int(t*100+1)):
        dexgp.set_motor_power(dexgp.MOTOR_LEFT, 0)
        dexgp.set_motor_power(dexgp.MOTOR_RIGHT,100)
        time.sleep(0.01)
    dexgp.set_motor_power(dexgp.MOTOR_LEFT + dexgp.MOTOR_RIGHT, 0)


def ltd(d):
    """
    Turns left for d degrees.

    Example:
    import AOLMERobots as gopi
    gopi.ltd(30)
    """
    if DEBUG: 
        print("\tTurning left for",d,"degrees")
    easygpg3 = easy.EasyGoPiGo3()
    dexgp = gopigo3.GoPiGo3()
    easygpg3.turn_degrees(-d, True)
    dexgp.set_motor_power(dexgp.MOTOR_LEFT + dexgp.MOTOR_RIGHT, 0)
    

    
def rtd(d):
    """
    Turns right for d degrees.

    Example:
    import AOLMERobots as gopi
    gopi.ltd(30)
    """
    if DEBUG:
        print("\tTurning right for",d,"degrees")
    easygpg3 = easy.EasyGoPiGo3()
    dexgp = gopigo3.GoPiGo3()
    easygpg3.turn_degrees(d, True)
    dexgp.set_motor_power(dexgp.MOTOR_LEFT + dexgp.MOTOR_RIGHT, 0)


"""
              Distance sensor
"""
def get_dist():
    """
    Returns obstacle distance in mm (milli meter).

    Example:
      import AOLMERobots as gopi
      dist = gopi.get_dist()
      print(dist)
    """
    if DEBUG:
        print("\tReturns distance of obstacle")
    easy_gpg           = easy.EasyGoPiGo3()
    my_distance_sensor = easy_gpg.init_distance_sensor()
    dist               = my_distance_sensor.read_mm()
    return dist


"""
             Robot Camera
"""

def get_image(image_name):
    """
    Returns an image taken using raspberry pi camera.
    This image can be directly used with OpenCV library.
    """
    if DEBUG:
        print("\tTakes image using camera")
    camera    = PiCamera()
    camera.resolution = (512,512)
    raw_img   = PiRGBArray(camera)
    time.sleep(0.1) # Let camera warm up
    camera.capture(raw_img, format="bgr")
    camera.close()
    image     = raw_img.array
    return image

    
def save_image(img, image_name):
    """
    Saves image at /home/pi/robo_snap/ directory.
    """
    if DEBUG:
        print("\tSaves image at /home/pi/robo_snap/")
    cv2.imwrite("/home/pi/robo_snap/"+image_name+'.png',img)


def show_RGB_hist(img):
    """
    Show the image and the RGB histograms.
    """
    if DEBUG:
        print("\Show an image and its red/green/blue histograms")
    
    cv2.imshow("Figure1",img)
    cv2.moveWindow("Figure1", 10,10);
    cv2.waitKey(1000)
    th = threshold(img)
    th.show_color_histograms()

def show_image(img):
    """
    Show image.
    """
    if DEBUG:
        print("\tShows image for 10 milli seconds")
    cv2.imshow("Figure1",img)
    cv2.moveWindow("Figure1", 10,10);
    cv2.waitKey(10)


def get_image_center():
    """
    Returns coordinates of image center.
    """
    if DEBUG:
        print("\tCalculates image center")
    camera    = PiCamera()
    camera.resolution = (512,512)
    raw_img   = PiRGBArray(camera)
    time.sleep(0.1) # Let camera warm up
    camera.capture(raw_img, format="bgr")
    camera.close()
    image     = raw_img.array
    image_ht  = image.shape[0]
    image_wd  = image.shape[1]
    return image_wd/2,image_ht/2


def get_object_center(rth, gth, bth):
    """
    Returns centroid of the object detected using
    color thresholds.
    """
    if DEBUG:
        print("\tGets object center")
        
    camera    = PiCamera()
    camera.resolution = (512,512)
    raw_img   = PiRGBArray(camera)
    time.sleep(0.1) # Let camera warm up
    camera.capture(raw_img, format="bgr")
    camera.close()
    img       = raw_img.array

    thr_obj               = threshold(img)
    thr_obj.sel_color_comp('red')
    RedRange              = thr_obj.ThreshRange (rth[0], rth[1])
    thr_obj.sel_color_comp('green')
    GreenRange            = thr_obj.ThreshRange (gth[0], gth[1])
    thr_obj.sel_color_comp('blue')
    BlueRange             = thr_obj.ThreshRange (bth[0], bth[1])
    (obj_center, ang, img) = comb_thr(img, BlueRange, GreenRange, RedRange, 'Vision', 90, 'test').returnResults()
    if (len(obj_center) == 0):
        x = random.randint(0,img.shape[1]/2)
        y = random.randint(0,img.shape[0]/2)
    else:
        x = obj_center[0]
        y = obj_center[1]
    return x,y,img
    

"""
           Robot Controls
"""
def reset_sensors():
    """
    Resets sensors
    """
    if DEBUG:
        print("\tResets all gopigo sensors")
    dexgp = gopigo3.GoPiGo3()
    dexgp.reset_all()
