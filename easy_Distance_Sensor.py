import time
import easygopigo3 as easy

gpg = easy.EasyGoPiGo3()


my_distance_sensor = gpg.init_distance_sensor()

while True:

    print("Distance Sensor Reading (mm): " + str(my_distance_sensor.read_mm()))
