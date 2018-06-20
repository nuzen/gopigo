import AOLMERobots as gopi
from datetime import datetime
from random import randint
import pdb

# Starting timer
start_time = datetime.now()

# Resetting all sensors
gopi.reset_sensors()

# Initializing time difference
current_time    = datetime.now()
time_diff       = current_time - start_time
time_diff_sec   = time_diff.total_seconds()

# Robot runs for 10 seconds
while(time_diff_sec <= 10):
    
    dist = gopi.get_dist()            # Get initial distance
    print("Distance = "+str(dist))
    if(dist > 100):                   # If distance > 100 mm
        gopi.fw(1)                    #    Move forward for 1 second
    else:                             # Else
        rand_num = randint(0,2)       #    Generate random number between 0 and 2
        if rand_num == 0:             #      If random number is 0
            gopi.rtd(30)              #        right turn 30 degrees
        elif rand_num == 1:           #      IfElse random number is 1
            gopi.ltd(30)              #        left turn 30 degrees
        else:                         #      Else
            gopi.bw(1)                #        go back for 1 second
            
    # Update time
    current_time  = datetime.now()
    time_diff     = current_time - start_time
    time_diff_sec = time_diff.total_seconds()
    
# Resetting all sensors
gopi.reset_sensors()
    
    
