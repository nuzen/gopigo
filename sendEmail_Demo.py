"""
DESCRIPTION:
 The following program demonstrates taking picture
 and sending it via email. In case the  picture name
 is not mentioned the default is taken to be the latest
 in './pics' directory.
 
 Email is received to aolme.pigopi@gmail. The title
 is <Your robot name>_Picture.


NOTE:
 - Images are expected to be in 'png' format.
 - Students are encouraged to use Method 3.
"""


import aolme

"""
Method 1:
 Here we do not provide name when taking
 picture and sending it via email.
"""
aolme.TakeSnap()
aolme.sendEmail()

"""
Method 2:
 We provide name for the picture when taking
 but donot provide when sending. Since the
 default is latest we email correct one.
"""
aolme.TakeSnap("snap1")
aolme.sendEmail()

"""
Method 3: ---> ENCOURAGED TO USE
 We provide name when taking the picture as
 well as sending. 
"""
aolme.TakeSnap("snap2")
aolme.sendEmail("snap2")
