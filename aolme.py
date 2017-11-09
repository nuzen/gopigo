""""
Provides basic movement and Video funtionality.
"""
import time
import datetime
import gopigo3
import easygopigo3 as easy
import glob
import os
import pygame
# Camera and Image processing modules.
from picamera.array import PiRGBArray
from picamera import camera
from picamera import PiCamera
import cv2
from thresholds2 import threshold, comb_thr
# Email modules.
import socket # To get hostname
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

# Creating driver class object, provided by dexter labs.
dexgp = gopigo3.GoPiGo3() 
easygpg = easy.EasyGoPiGo3()
startTime = 0
#
#                           Movement
#
def fw(t):
    for i in range(0, int(t*100+1) ):
        dexgp.set_motor_power(dexgp.MOTOR_LEFT + dexgp.MOTOR_RIGHT, 100)
        time.sleep(0.01)
    #dexgp.reset_all()
    
def bw(t):
    for i in range(0, int(t*100+1) ):
        dexgp.set_motor_power(dexgp.MOTOR_LEFT + dexgp.MOTOR_RIGHT, -100)
        time.sleep(0.01)
    #dexgp.reset_all()

def leftsec(t): ## chabge for degreees
    for i in range(0, int(t*100+1)):
        dexgp.set_motor_power(dexgp.MOTOR_RIGHT, 50)
        dexgp.set_motor_power(dexgp.MOTOR_LEFT, 0)
        time.sleep(0.01)
    #dexgp.reset_all()

def lt(degrees):
    dexgp.turn_degrees(-degrees)
    #dexgp.reset_all()
    
def rt(degrees):
    dexgp.turn_degrees(degrees)
    #dexgp.reset_all()
          
def rightsec(t):
    """
    Moves the robot right for t seconds.
    """
    for i in range(0, int(t*100+1) ):
        dexgp.set_motor_power(dexgp.MOTOR_LEFT, 50)
        dexgp.set_motor_power(dexgp.MOTOR_RIGHT, 0)
        time.sleep(0.01)
    #dexgp.reset_all()



#
#                           Vision
#
def color_det():
    cd = color()
    cd.process_camera()

def getPic():
    """
    Returns a picture captured via raspberry pi camera.
    """
    # initialize the camera and grap a reference to the raw
    # camera capture
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)

    # allow the camra to warmup
    time.sleep(0.1)

    #grab an image from the camera
    camera.capture(rawCapture, format='bgr')
    image = rawCapture.array
    camera.close()
    return image

def getImgCenter(img):
    """
    Returns the coordinates of image center. The image
    is assumed to have,
      Top left     = (0,0)
      Bottom right = (image height, image width)
    
    The coordinates returned (row position, col position).
    """
    ht, wd, ch = img.shape
    center = [wd/2, ht/2]
    return center

def getObjCenter(img, MMA):
    """
    MMA[i] = MinMaxArray,
      i       Def
      -------------------
      0       RedLowValue
      1       RedHiValue
      2       GreenLowValue
      3       GreenHiValue
      4       BlueLowValue
      5       BlueHiValue
    """
    thr_obj = threshold(img)
    thr_obj.sel_color_comp('red')
    RedRange = thr_obj.ThreshRange (MMA[0], MMA[1])
    thr_obj.sel_color_comp('green')
    GreenRange = thr_obj.ThreshRange (MMA[2], MMA[3])
    thr_obj.sel_color_comp('blue')
    BlueRange = thr_obj.ThreshRange (MMA[4], MMA[5])
    (objCenter, Ang, img) = comb_thr(img, BlueRange, GreenRange, RedRange, 'Helloworld', 1, 'test').returnResults()
#    cv2.imshow('Temp',img)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
    return objCenter

def TakeSnap(name=''):
    if len(name) == 0:
        today = datetime.datetime.today().strftime('%m%d%Y')
        time = datetime.datetime.now().strftime('%H%M')
        name = str(today)+'_'+str(time)
    with PiCamera() as cam:
        cam.capture('./pics/'+name+'.png')

#    
#                           Audio and beep
#
my_buzzer = gopigo3.Buzzer("AD2", dexgp)
def play_mp3(name):
    namemp3='{}.mp3'.format(name)
    pygame.mixer.init()
    pygame.mixer.music.load(namemp3)
    pygame.mixer.music.play()
    #while pygame.mixer.music.get_busy() == True:
    #    continue
    
def beep1():
    my_buzzer.sound(my_buzzer.scale["E4"])
    time.sleep(0.5)
    my_buzzer.sound_off()

def beep2():
    my_buzzer.sound(my_buzzer.scale["E4"])
    time.sleep(0.5)
    my_buzzer.sound(my_buzzer.scale["B4"])
    time.sleep(0.5)
    my_buzzer.sound_off()

def beep3():
    my_buzzer.sound(my_buzzer.scale["C4"])
    time.sleep(0.5)
    my_buzzer.sound(my_buzzer.scale["G4"])
    time.sleep(0.5)
    my_buzzer.sound(my_buzzer.scale["C4"])
    time.sleep(0.5)
    my_buzzer.sound(my_buzzer.scale["G4"])
    time.sleep(0.5)
    my_buzzer.sound_off()

def beepLong():
    ode = ["E4","E4","F4","G4","G4","F4","E4","C4"]
  #  ode = ["E4", "E4", "F4", "G4", "G4"]
    for note in ode:
        print(note)
        my_buzzer.sound(my_buzzer.scale[note])
        time.sleep(0.3)
        my_buzzer.sound_off()
        time.sleep(0.15)
    my_buzzer.sound_off()
    
#
#                           Distance sensor
#
def getDist():
    """
    Returns the distance in millimeter.
    """
    my_distance_sensor = easygpg.init_distance_sensor()
    dist = my_distance_sensor.read()
    return dist

def printDist():
    """
    Prints distance in mm, cm, m and inches.
    """
    my_distance_sensor = easygpg.init_distance_sensor()
    print("Distance Sensor Reading (mm): " + str(my_distance_sensor.read_mm()))
    print("Distance Sensor Reading (cm): " + str(my_distance_sensor.read()))
    print("Distance Sensor Reading (m): " + str(my_distance_sensor.read()/100))
    print("Distance Sensor Reading (inches): " + str(my_distance_sensor.read_inches()))

#
#                         Control functions
#
def resetSensors():
    """
    Resets all the sensors
    """
    dexgp.reset_all()
def startTimer():
    """
    Stores the starting time
    """
    global startTime
    startTime = time.time()
    
def elapsedTime():
    """
    Returns time elapsed after
    the clock is started in seconds.
    """
    global startTime
    elapsedTime = time.time() - startTime
    return elapsedTime

def goToBed():
    """
    Shuts down robot after playing
    some sound via buzzer.
    """
    print('Not implemented yet')

#
# Email
#
def check_attach(fileToSend):
    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)
    fp = open(fileToSend, "rb")
    attachment = MIMEImage(fp.read(), _subtype=subtype)
    fp.close()
    return attachment
    
def sendEmail(fileName=''):
    hostName = socket.gethostname()
    if len(fileName) == 0:
        fileList = glob.glob('./pics/*.png')
        fileName = max(fileList, key=os.path.getctime)
    else:
        fileName = './pics/'+fileName+'.png'
    emailfrom = "aolmegopigo3@gmail.com"
    emailto = ["aolme.gopigo@gmail.com"] # Password is pigopi123!
    fileToSend = fileName
    username = "aolmegopigo3"
    password = "robots1234"
    body = 'Hi, Please find '+fileName+' attached.'
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = ", ".join(emailto)
    msg["Subject"] = hostName +  '_Picture'
    msg.attach(MIMEText(body, 'plain'))
    attachment = check_attach(fileToSend)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(username,password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()
    print('Email successfully sent from '+hostName+' with '
          +fileName)
