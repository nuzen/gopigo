from AOLMERobots import *

# Reset all sensors
reset_sensors()

# initialize time
cur_time = get_time()

# Run for no more than 2 minutes
while(cur_time < 10):
	
	# measure distance to object
	dist = get_dist()
	
	# print distance to object
	print("Distance =",dist)
	
	# if distance is greater than xxx mm
	#    Move forward
	# else
	#    turn
	if dist > 100:
		fw(1)
	else:
		rt(0.3)
	
	# update time
	cur_time = get_time()
