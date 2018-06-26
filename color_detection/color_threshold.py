# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 10:00:44 2018

@author: AOLME_2
"""

import AOLMERobots as gopi
# Resetting all sensors
gopi.reset_sensors()

img = gopi.get_image('Figure')
gopi.show_RGB_hist(img)