"""
DESCRIPTION:
 The following program demonstrates taking picture
 and sending it via email.
 
 Email is received to aolme.pigopi@gmail. The title
 is <Your robot name>_Picture.


NOTE:
 - Images are expected to be in 'png' format.
 - Students are encouraged to use Method 3.
"""


from AOLMERobots import get_image, save_image, send_email
"""
 We provide name when taking the picture as
 well as sending. 
"""
email_address = "venkatesh.jatla@gmail.com"
img    = get_image()
save_image(img, "my_image")
send_email(email_address, "my_image.png")
