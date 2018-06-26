import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

import AOLMERobots as gopi
from thresholds2 import *
import cv2



    

   

class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'Name of the image'
        self.left = 200
        self.top = 200
        self.width = 400
        self.height = 140
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,40)
 
        # Create a button in the window
        self.button = QPushButton('Upload', self)
        self.button.move(20,80)
 
        # connect button to function on_click
        self.button.clicked.connect(self.get_text)
        self.show()
 
    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")
        return
    
    def get_text(self):
        
        print(self.textbox.text())
        image = cv2.imread((self.textbox.text()))
         #gopi.show_image(img)
         # Constructor for threshold class:
        thr_obj = threshold(image)
        #cv2.namedWindow('image')
    
##        def nothing(x):
##            pass
##        # create trackbars for color change
##
##        cv2.createTrackbar('RL','image',0,255,nothing)
##        cv2.createTrackbar('RH','image',0,255,nothing)
##
##        cv2.createTrackbar('GL','image',0,255,nothing)
##        cv2.createTrackbar('GH','image',0,255,nothing)
##
##        cv2.createTrackbar('BL','image',0,255,nothing)
##        cv2.createTrackbar('BH','image',0,255,nothing)
##
##        # Blue component processing:
##        thr_obj.sel_color_comp ('blue')
##        ##LowValue  =  0     # Use blue histogram to determine low value
##        ##HiValue   =  255   # Use blue histogram to determine high value,
##                 # thresh to 255 removes all regions less than or equal to 255.
##
##
##        print(1)
##        while(1):
##    
##            k = cv2.waitKey(1) & 0xFF
##            if k == 27:
##                break
##
##            img = image.copy()    
##            # get current positions of four trackbars
##    
##            redLow = cv2.getTrackbarPos('RL','image')
##            redHi = cv2.getTrackbarPos('RH','image')
##    
##            greenLow = cv2.getTrackbarPos('GL','image')
##            greenHi = cv2.getTrackbarPos('GH','image')
##        
##            blueLow = cv2.getTrackbarPos('BL','image')
##            blueHi = cv2.getTrackbarPos('BH','image')
##    
##            rgb_values = [blueLow, blueHi, greenLow, greenHi, redLow, redHi]
##    
##            RedLow   =  thr_obj.ThreshLow   (redLow)            
##            RedRange =  thr_obj.ThreshRange (redLow , redHi)   
##            RedHi    =  thr_obj.ThreshHigh  (redHi)
##    
##            print(2)
##            RedLow_single = thr_obj.single_color(RedLow, 'r')
##            RedRange_single = thr_obj.single_color(RedRange, 'r')
##            RedHi_single = thr_obj.single_color(RedHi, 'r')
##    
##            GreenLow   =  thr_obj.ThreshLow   (greenLow)            
##            GreenRange =  thr_obj.ThreshRange (greenLow , greenHi)   
##            GreenHi    =  thr_obj.ThreshHigh  (greenHi)
##    
##            GreenLow_single = thr_obj.single_color(GreenLow, 'g')
##            GreenRange_single = thr_obj.single_color(GreenRange, 'g')
##            GreenHi_single = thr_obj.single_color(GreenHi, 'g')
##    
##            BlueLow   =  thr_obj.ThreshLow   (blueLow)            
##            BlueRange =  thr_obj.ThreshRange (blueLow , blueHi)   
##            BlueHi    =  thr_obj.ThreshHigh  (blueHi)             
##   
##            BlueLow_single = thr_obj.single_color(BlueLow, 'b')
##            BlueRange_single = thr_obj.single_color(BlueRange, 'b')
##            BlueHi_single = thr_obj.single_color(BlueHi, 'b')
##   
##    
##            #gopi.show_RGB_hist(img, rgb_values)
##   
##            white= np.zeros((90, RedLow.shape[1], 3), np.uint8)
##            white[:] = (255)
##  
##            #cv2.resizeWindow('image', 200,200)
##            vcat1 = cv2.vconcat((white, RedLow_single))
##            vcat2 = cv2.vconcat((white, RedRange_single))
##            vcat3 = cv2.vconcat((white, RedHi_single))
##            print(3)
##            vcat4 = cv2.vconcat((white, GreenLow_single))
##            vcat5 = cv2.vconcat((white, GreenRange_single))
##            vcat6 = cv2.vconcat((white, GreenHi_single))
##    
##            vcat7 = cv2.vconcat((white, BlueLow_single))
##            vcat8 = cv2.vconcat((white, BlueRange_single))
##            vcat9 = cv2.vconcat((white, BlueHi_single))
##    
##            font = cv2.FONT_HERSHEY_SIMPLEX
##            cv2.putText(vcat1,'0<=v<RL',(30,50), font, 1.5,(0,0,0), 3, 0)
##            cv2.putText(vcat2,'RL<=v<=RH',(30,50), font, 1.5,(0,0,0), 3, 0)
##            cv2.putText(vcat3,'RH<v<=255',(30,50), font, 1.5,(0,0,0), 3, 0)
##            cv2.putText(vcat4,'0<=v<GL',(30,50), font, 1.5,(0,0,0), 3, 0)
##            cv2.putText(vcat5,'GL<=v<=GH',(30,50), font, 1.5,(0,0,0), 3, 0)
##            cv2.putText(vcat6,'GH<v<=255',(30,50), font, 1.5,(0,0,0), 3, 0)
##            cv2.putText(vcat7,'0<=v<BL',(30,50), font, 1.5,(0,0,0), 3, 0)
##            cv2.putText(vcat8,'BL<=v<=BH',(30,50), font, 1.5,(0,0,0), 3, 0)
##            cv2.putText(vcat9,'BH<v<=255',(30,50), font, 1.5,(0,0,0), 3, 0)
##        
##            red_all = np.hstack((vcat1, vcat2, vcat3))
##            green_all = np.hstack((vcat4, vcat5, vcat6))
##            blue_all = np.hstack((vcat7, vcat8, vcat9))
##    
##            rgb_all = np.vstack((red_all, green_all, blue_all))
##
##    
##            print(4)
##            comb_image = thr_combination(img, BlueRange,GreenRange, RedRange).return_result()   
##    
##            red_min_max = [redLow, redHi]
##            grn_min_max = [greenLow, greenHi]
##            blu_min_max = [blueLow, blueHi]
##    
##            x,y,det_img, max_area = gopi.get_img_object_center(img, red_min_max, grn_min_max, blu_min_max)
##            white_2= np.zeros((90+RedLow.shape[0], 2*RedLow.shape[1], 3), np.uint8)
##            white_2[:] = (255)    
##    
##            cv2.putText(white_2, str(redLow) +'<= Red <= '+str(redHi),(30,150), font, 1.5,(0,0,0), 3, 0)
##            cv2.putText(white_2, str(greenLow)+ '<= Green <='+str(greenHi),(30,220), font, 1.5,(0,0,0), 3, 0)
##            cv2.putText(white_2, str(blueLow) +'<= Blue <='+str(blueHi),(30, 290), font, 1.5,(0,0,0), 3, 0)
##            cv2.putText(white_2,'LargestArea = '+str(int(max_area)),(30,360), font, 1.5,(0,0,0), 3, 0)
##    
##            plot_1 = np.vstack((white, comb_image))
##    
##            cv2.putText(plot_1,'Middle RGB Combination',(10,50), font, 1.2,(0,0,0), 3, 0)
##            plot_2 = np.hstack((plot_1, white_2))
##            plot_3 = np.vstack((rgb_all, plot_2))
##    
##    
##            print(5)
##            cv2.namedWindow('RGB binary',0)
##            cv2.moveWindow('RGB binary', 515,37);
##            cv2.imshow('RGB binary', plot_3)
##            cv2.resizeWindow('RGB binary', 700,900)
##    
##    
##            cv2.imshow('image',det_img)
##     
##            cv2.waitKey(1000)
##            gopi.show_RGB_hist(img, rgb_values)    
##    
##    
##        #cv2.destroyAllWindows()

        return 
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
  
    
    