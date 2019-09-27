#
#      ██╗███████╗████████╗████████╗   ███████╗███████╗███╗   ██╗
#      ██║██╔════╝╚══██╔══╝╚══██╔══╝   ██╔════╝██╔════╝████╗  ██║
#      ██║█████╗     ██║      ██║█████╗███████╗█████╗  ██╔██╗ ██║
# ██   ██║██╔══╝     ██║      ██║╚════╝╚════██║██╔══╝  ██║╚██╗██║
# ╚█████╔╝███████╗   ██║      ██║      ███████║███████╗██║ ╚████║
#  ╚════╝ ╚══════╝   ╚═╝      ╚═╝      ╚══════╝╚══════╝╚═╝  ╚═══╝
#
#   Sensorized Panasonic Jetter Hackable Bike
#   Andres Rico - MIT Media Lab - aricom@mit.edu - www.andresrico.xyz
#
#   Main script for collecting data from Camera Module.
#   Data consists of a timestamped RGB image vector taken every second.
#   This script can work in parallel with GPS and Camera data collection scripts (gps_main.py & camera.py)

import time
import picamera                                                                 #Used for camera module operation.
import numpy as np
import sys
import datetime                                                                 #Used for time stamps.
import subprocess                                                               #Allows subprocess calls.


#Function
def get_image():
    with picamera.PiCamera() as camera:
        camera.resolution = (640,480)                                           #Set camera resolution. Can be changed depending on ML demands.
        camera.framerate = 24
        time.sleep(1)
        image = np.empty((480, 640, 3) , dtype = np.uint8)                      #Create empty 3D numpy array.
        #image.setflags(write=True)
        camera.capture(image, 'bgr')                                            #Capture RGB data.
        return image                                                            #Return RGB data within 3D np array.


#Function for checking status of headlight for activation of data collection.
#Data collection is enabeled by turning on headlights.
def data_activation():
    path = '/home/pi/hackbikeARICOM/cmd'
    data_active = subprocess.check_output([ path + '/getHeadLight' , '-1'], shell=True) #Gets HeadLight Status (0 = OFF , 1 = ON)
    return float(data_active)                                                   #Returns float with headlight value.



if __name__== "__main__":

    main_path = '/home/pi/hackbikeARICOM/'                                      #Declare main path for scripts.
    data_path = '/home/pi/hackbikeARICOM/camera_data/'                          #Declare path for storing data files.

    print ('Camera has been activated')

    print("Ready To Collect images!")

    subprocess.call(['sudo python3 ' + main_path +  'data_indicator_light.py 3' , '-1'], shell=True) #Turn light green when GPS has been activated.

    data_acquisition = False #Variable for activation and deactivation of data collection.

    while True: #Main loop.
        if data_acquisition == False and data_activation() == 1: #Check if headlight has been activated.
                data_acquisition = True
                datestring = str(datetime.datetime.now())
                datestring = datestring + ".txt"
                new_file = open(data_path + datestring,"w")                     #Open file with timestamp name when data collection has beeen enabeled.
                print("Image Collection Enabeled")

        if data_acquisition == True and data_activation() == 0: #Check for headlight deactivation to shutdown data colection.
                data_acquisition = False
                new_file.close()
                print("Image Collection Diabeled")

        if data_acquisition == True: #Enter if data collection is active.
            timestamp = str(datetime.datetime.now().time())                     #Create time stamp string.
            current_image = get_image()
            current_image = str(repr(current_image.flatten()))                  #Flattens 3D numpy array into 1D vector.
            current_image = current_image[7:-15]                                #reformats data points.
            print(timestamp[:11] + " , " + current_image)
            new_file.write(timestamp[:11] + "," + current_image)                #Writes data into new file.
