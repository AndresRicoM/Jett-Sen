import time
import picamera
import numpy as np
import sys
import datetime
import subprocess

def get_image():
    with picamera.PiCamera() as camera:
        camera.resolution = (640,480)
        camera.framerate = 24
        time.sleep(1)
        image = np.empty((480, 640, 3) , dtype = np.uint8)
        #image.setflags(write=True)
        camera.capture(image, 'bgr')
        return image
        
                
def data_activation():
    path = '/home/pi/hackbikeARICOM/cmd'
    data_active = subprocess.check_output([ path + '/getHeadLight' , '-1'], shell=True)
    return float(data_active)

        

if __name__== "__main__":
    
    main_path = '/home/pi/hackbikeARICOM/'
    data_path = '/home/pi/hackbikeARICOM/camera_data/'
    
    print ('Camera has been activated')
    
    print("Ready To Collect images!")

    subprocess.call(['sudo python3 ' + main_path +  'data_indicator_light.py 3' , '-1'], shell=True)

    data_acquisition = False #Variable for activation and deactivation of data collection.

    while True: #Main loop.
        if data_acquisition == False and data_activation() == 1: #Check if touch sensor has been activated. 
                data_acquisition = True
                datestring = str(datetime.datetime.now())
                datestring = datestring + ".txt"
                new_file = open(data_path + datestring,"w")
                #subprocess.call(['sudo python3 /home/pi/hackbikeARICOM/data_indicator_light.py 0' , '-1'], shell=True)
                print("Image Collection Enabeled")
                
        if data_acquisition == True and data_activation() == 0: #Check for sensor activation to shutdown data colection. 
                data_acquisition = False
                #time.sleep(.4)
                new_file.close()
                #subprocess.call(['sudo python3 /home/pi/hackbikeARICOM/data_indicator_light.py 1' , '-1'], shell=True)
                print("Image Collection Diabeled")
                #time.sleep(2)
                
        if data_acquisition == True: #Enter if data collection is active.
            timestamp = str(datetime.datetime.now().time())
            current_image = get_image()
            current_image = str(repr(current_image.flatten()))
            current_image = current_image[7:-15]
            print(timestamp[:11] + " , " + current_image)
            new_file.write(timestamp[:11] + "," + current_image)
