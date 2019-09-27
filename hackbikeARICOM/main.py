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
#
#
#
#
#


import RPi.GPIO as GPIO #Import Library for GPIO Communication.
import time
import Termite_Access
import time
from time import sleep
import datetime
import subprocess
import pigpio
import difflib

def data_activation():
    path = '/home/pi/hackbikeARICOM/cmd'
    data_active = subprocess.check_output([ path + '/getHeadLight' , '-1'], shell=True)
    return float(data_active)

def getBikeData():
    path = '/home/pi/hackbikeARICOM/cmd'
    headlightData = subprocess.check_output([path + '/getHeadLight' , '-1'], shell=True)
    headlightData = [float(headlightData[0])] #State of Headlight

    #print(headlightData)

    #Get Battery State Data.
    batteryData = subprocess.check_output([path + '/getBattery' , '-1'], shell=True)

    battery_list = []
    for t in batteryData.split():
        try:
            battery_list.append(float(t))
        except ValueError:
            pass

    #print(battery_list)

    #Get Crank State Data.
    crankData = subprocess.check_output([path + '/getCrank' , '-1'], shell=True)

    crank_list = []
    for t in crankData.split():
        try:
            crank_list.append(float(t))
        except ValueError:
                pass

    #print(crank_list)

    #Get Drive State Date.
    driveData = subprocess.check_output([path + '/getDrive' , '-1'], shell=True)

    drive_list = []
    for t in driveData.split():
        try:
            drive_list.append(float(t))
        except ValueError:
            pass

    #print(drive_list)

    #Get Mode State Data.
    modeData = subprocess.check_output([ path + '/getMode' , '-1'], shell=True)

    mode_list = []
    for t in modeData.split():
        try:
            mode_list.append(float(t))
        except ValueError:
            pass

    complete_data = []
    complete_data.extend(headlightData)
    complete_data.extend(battery_list)
    complete_data.extend(crank_list)
    complete_data.extend(drive_list)
    complete_data.extend(mode_list)

    return complete_data


if __name__== "__main__":

    main_path = '/home/pi/hackbikeARICOM/'
    data_path = '/home/pi/hackbikeARICOM/data/'
    print("TerMITe Connecting....")
    TF = Termite_Access.termiteObject() #Find a terMITe.
    TF.activateCSV() #Swith terMITe output to CSV - Can choose JSON as well.

    print("Ready To Collect Data!")

    subprocess.call(['sudo python3 ' + main_path +  'data_indicator_light.py 1' , '-1'], shell=True)

    data_acquisition = False #Variable for activation and deactivation of data collection.

    while True: #Main loop.
        if data_acquisition == False and data_activation() == 1: #Check if touch sensor has been activated.
                data_acquisition = True
                #time.sleep(.4)
                datestring = str(datetime.datetime.now())
                datestring = datestring + ".txt"
                new_file = open(data_path + datestring,"w")
                subprocess.call(['sudo python3 /home/pi/hackbikeARICOM/data_indicator_light.py 0' , '-1'], shell=True)
                print("Data Collection Enabeled")

        if data_acquisition == True and data_activation() == 0: #Check for sensor activation to shutdown data colection.
                data_acquisition = False
                #time.sleep(.4)
                new_file.close()
                subprocess.call(['sudo python3 /home/pi/hackbikeARICOM/data_indicator_light.py 1' , '-1'], shell=True)
                print("Data Collection Diabeled")
                #time.sleep(2)

        if data_acquisition == True: #Enter if data collection is active.
            timestamp = str(datetime.datetime.now().time())
            bikeData = str(getBikeData())
            bikeData = bikeData[1:-1]
            #bikeData = bikeData[:-1]
            print(timestamp[:11] + " , " + bikeData + " , " + TF.termiteValue)
            new_file.write(timestamp[:11] + "," + bikeData  + " , " + TF.termiteValue) #Write terMITe data with timestamp.
            #print(TR.termiteValue)
            time.sleep(0.4)
