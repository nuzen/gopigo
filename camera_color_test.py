# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 22:51:38 2017

@author: Wenjing Shi
"""
import matplotlib.pyplot as pyplot
import numpy as np
from matplotlib import pyplot as plt
import gopigo3
import pygame
import time
import easygopigo3 as easy
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from thresholds2 import threshold, comb_thr
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

dexgp = gopigo3.GoPiGo3() # Creating driver class object, provided by dexter labs.
my_buzzer = gopigo3.Buzzer("AD2", dexgp)

class color:
    def __init__(self):

        self.action = input('Action ("test" / "det"): ')
        if (self.action == 'det' or self.action == 'test'):
            self.message = input('Secret message: ')
            self.BlueLowValue = float(input('BlueLowValue: '))
            self.BlueHiValue = float(input('BlueHiValue: '))
            self.GreenLowValue = float(input('GreenLowValue: '))
            self.GreenHiValue = float(input('GreenHiValue: '))
            self.RedLowValue = float(input('RedLowValue: '))
            self.RedHiValue = float(input('RedHiValue: '))
            self.N = 1
            self.num_img = 1
        else:
            print ('Warning: Wrong action.')
            return

    def take_pic(self, image, image_det):

        ori_filename = 'pics//frame_'+str(self.num_img)+'.png'
        img_filename = 'pics//frame_det'+str(self.num_img)+'.png'
        cv2.imwrite(ori_filename , image)
        cv2.imwrite(img_filename, image_det)
        self.num_img = self.num_img + 1
        return (ori_filename, img_filename)

    def check_attach(self, fileToSend):
        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
        
            
        return attachment
        
    def send_mail(self, ori_filename, img_filename):
    
        emailfrom = "aolmegopigo3@gmail.com"

        #emailto = ["wshi@unm.edu", "pattichis@gmail.com", "luis2arm@gmail.com"]
        emailto = ["wshi@unm.edu"]
        fileToSend = ori_filename
        fileToSend_1 = img_filename
        #fileToSend = "aolme.py"
        username = "aolmegopigo3"
        password = "robots1234"
        body = "Hi, this is your python mission! " + self.message
    
    
        msg = MIMEMultipart()
        msg["From"] = emailfrom
        msg["To"] = ", ".join(emailto)
        msg["Subject"] = "Message from GoPiGo_dex"
        #msg.preamble = "Wa hahaha"
        msg.attach(MIMEText(body, 'plain'))

        attachment = self.check_attach(fileToSend)
        attachment_1 = self.check_attach(fileToSend_1)
        
        attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
        attachment_1.add_header("Content-Disposition", "attachment", filename=fileToSend_1)
        
        msg.attach(attachment)
        msg.attach(attachment_1)
                    
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(username,password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()

    
        
    def analyze_pic(self, frame):
        image = frame.array
        thr_obj = threshold (image)
        
        thr_obj.sel_color_comp ('blue')
        BlueRange =  thr_obj.ThreshRange (self.BlueLowValue, self.BlueHiValue)   #  LowValue <= Blue <= HiValue
           
        # Green component processing:
        thr_obj.sel_color_comp('green')
        GreenRange =  thr_obj.ThreshRange (self.GreenLowValue, self.GreenHiValue) #  LowValue <= Green <= HiValue
           

        # Red component processing:
        thr_obj.sel_color_comp('red')
        RedRange =  thr_obj.ThreshRange (self.RedLowValue, self.RedHiValue) # LowValue <= Green <= HiValue
            
        (self.N, img) = comb_thr(image, BlueRange, GreenRange, RedRange, self.message, self.N, self.action).im_show()

        return img

    
    def process_camera(self):
       
        # initialize the camera and grab a reference to the raw camera capture
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera, size=(640, 480))
        cap = cv2.VideoCapture(0)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('videos//output.avi', fourcc, 5.0, (640, 480))
    
        # allow the camera to warmup
        time.sleep(0.1)
    
        # capture frames from the camera
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            ori_img = frame.array.copy()
            img = self.analyze_pic(frame)

            key = cv2.waitKey(1) & 0xFF

            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)
            
            # save the frame to video
            out.write(img)
            
            # if the 'a' key was pressed, take picture and save it together with the detection
            # one to the file in the file "/video/..."
            if key == ord("a"):
                self.take_pic(ori_img, img)
                
            if key == ord("e"):
                (ori_filename, img_filename) = self.take_pic(ori_img, img)
                self.send_mail(ori_filename, img_filename)
                
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                dexgp.reset_all()
                cv2.destroyAllWindows()
                break
           
        
    
    

       

                
