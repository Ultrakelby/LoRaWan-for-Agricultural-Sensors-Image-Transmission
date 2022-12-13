# Image Compression and Transmission Algorithm 
# By Kelby Fredrick
# Initializations

import sys
from PIL import Image
import PIL      # Allows us to compress the image(s)
import os       # General os system interfaces
import numpy    # For image -> string manipulation
import shutil   # Used to delete a full directory
import binascii # Will let us convert the image to a string of hex numbers
import glob     # Can fand all JPEG files in the source Directory
import io
import base64
import time
import serial
import Jetson.GPIO as GPIO
import time
import serial
import Jetson.GPIO as GPIO
import sys

Parent_Directory = (r"/home/kelby/Desktop/main")
os.chdir(Parent_Directory) # Change the Value for the Parent Directory later

dir(Image)

#Import Image
im = Image.open("Cotton.jpg")
print(f"The image size dimensions are: {im.size}")

# Create a Temp Directory 
Parent_Directory = os.getcwd() # Find the File Path
print ("The current working directory is %s" % Parent_Directory) 

temp_dir = "Photo_Strings" # Temp Directory

try:
    os.mkdir(temp_dir)
except OSError: # Look for an error when creating the dir
    print ("Creation of the directory %s is failed" % temp_dir)
else:
    print ("Successfully created the directory %s " % temp_dir)
    
# Compression 
file_name = 'Cotton_compressed.jpg'
picture = Image.open('Cotton.jpg')
dim = picture.size
print(f"This is the current width and height of the image: {dim}")
picture.save(file_name,optimize=True,quality=30)

# Move the Compressed Image to temp_dir
shutil.copy(file_name,temp_dir)
os.remove(file_name)

# Change Path to New Directory and save compressed photo to 
new_path = os.chdir(temp_dir) #Change to temp Directory

new_path = os.getcwd() 
print ("The current working directory is %s" % new_path) 

# This is where we will cut the images into hex strings
file_name = 'Cotton_compressed.jpg'
with open(file_name, 'rb') as f:
    hex_string = f.read()
hex_string = binascii.hexlify(hex_string)

print(hex_string) # Allows us to see the Hex String in bytes if we wanted 
# b'' Means the following characters are bytes

# Divide compressed images into smaller more manageable strips
hex_string = hex_string.decode('UTF-8') # Decode bytes into a string
print(hex_string)

#print('\n')

#data = hex_string
#data = [data[i:i+25] for i in range(0, len(data), 2)] # Breaks string into smaller strips

# If I want to break the string into multiple variables >>

#var_holder = {}
 
#for i in range(0, len(data), 2):
#    var_holder['string_' + str(i)] = data[i]

#print(i)
 
#locals().update(var_holder)
 
#print(string_25416)

# Test cell to convert Hex bytes back to RGB Image

# integers = []

# while hex_string:
#   value = int.append(value)
#    hex_string = hex_string[2:]

#data = bytearray(integers)    
#     
#with open('output.jpg', 'wb') as fh:
#    print(fh.write(data))
     
#Remove the Temp Directory
#os.chdir(Parent_Directory) #Change back to Parent Directory

#path = os.getcwd()

#temp_dir = "Photo_Strings" # Temp Directory

#path = os.path.join(path, temp_dir)

#shutil.rmtree(path) # Remove the Temporary Directory filled with the photo strings 

#Done 
