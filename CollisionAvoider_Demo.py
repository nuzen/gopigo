"""
DESCRIPTION:

 Demonstrates the use of aolme library in programming
 collision avoidance.

ALGORITHM:

 Get distance from ultrasonic sensor.
 While (Time < 20 seconds) 
   IF distance is more than 25 mm 
     move for 1 second.
   Else 
     turn right for 45 degrees
   Update distance
"""
import aolme
aolme.resetSensors()   # reset all the sensors
aolme.startTimer()     # Start timer
dist = aolme.getDist() # initial distance
elapsedTime = aolme.elapsedTime() # initialize elapsedTime

while (elapsedTime < 20):             # Check if 20 seconds elapsed
    if dist > 25:                     # If distance > 25 mm
        aolme.fw(1)                   #   Move forward for 1 second
    else:                             # If distance < 25 mm
        aolme.lt(45)                  #   Turn right 45 degrees
    dist = aolme.getDist()            # Update distance after moving
    elapsedTime = aolme.elapsedTime() # new elapsedTime

aolme.resetSensors()  # Reset all the sensors
