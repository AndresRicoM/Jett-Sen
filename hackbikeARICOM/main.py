# -*- coding: UTF-8 -*-

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
#   Main script for collecting data from Panasonic Bike Module and MIT terMITe sensor.
#   Data from bike and data from environmental sensor are concatenated and stored within a timestamped file.
#   This script can work in parallel with GPS and Camera data collection scripts (gps_main.py & camera.py)


import RPi.GPIO as GPIO                                                         #Import Library for GPIO Communication.
import Termite_Access                                                           #Used for communication with terMITe sensor.
import time
from time import sleep
import datetime                                                                 #Used for timestamps.
import subprocess                                                               #Activates subprocess calls.
import pigpio
import difflib
import json

cmd_path = '/home/pi/hackbicycle/cmd'
is_bluetooth = False

#Function for checking status of headlight for activation of data collection.
#Data collection is enabeled by turning on headlights.
def data_activation():
    if is_bluetooth :
    	status_json_path = '/home/pi/status.json'
    	is_recording = False
    	with open(status_json_path, 'r') as f:
    	    try:
    	        status = json.load(f)
    	        is_recording = status['record']
    	    except ValueError:
    	        print("could not parse json data")
    	        pass
        return is_recording
    else:
    	path = '/home/pi/Jett-Sen/hackbikeARICOM/cmd'
    	data_active = subprocess.check_output([ path + '/getHeadLight' , '-1'], shell=True) #Gets HeadLight Status (0 = OFF , 1 = ON)
        #Returns float with headlight value.
    	return  int(data_active) == 1


#Function for extracting bike sensor data.
def getBikeData():
    # path = '/home/pi/Jett-Sen/hackbikeARICOM/cmd'                                        #Specifies path for Panasonic Bike commands.

    #headlightData = subprocess.check_output([path + '/getHeadLight' , '-1'], shell=True)       #Uncomment if headlight data is desired. In this implementation it will always be 1 when recording.
    #headlightData = [float(headlightData[0])] #State of Headlight

    #print(headlightData)

    #Get Battery State Data.
    batteryData = subprocess.check_output([cmd_path + '/getBattery' , '-1'], shell=True) #Call to extract battery data.

    battery_list = []
    for t in batteryData.split():                                               #Extracts numerical values from battery sensors by parsing command's output.
        try:
            battery_list.append(float(t))
        except ValueError:
            pass

    #print(battery_list)

    #Get Crank State Data.
    crankData = subprocess.check_output([cmd_path + '/getCrank' , '-1'], shell=True)#Call to extract Crank data.

    crank_list = []
    for t in crankData.split():                                                 #Extracts numerical values from crank sensors by parsing command's output.
        try:
            crank_list.append(float(t))
        except ValueError:
                pass

    #print(crank_list)

    #Get Drive State Date.
    driveData = subprocess.check_output([cmd_path + '/getDrive' , '-1'], shell=True)#Call to extract Drive data.

    drive_list = []
    for t in driveData.split():                                                 #Extracts numerical values from drive sensors by parsing command's output.
        try:
            drive_list.append(float(t))
        except ValueError:
            pass

    #print(drive_list)

    #Get Mode State Data.
    modeData = subprocess.check_output([ cmd_path + '/getMode' , '-1'], shell=True) #Call to extract Driving Mode data.

    mode_list = []
    for t in modeData.split():                                                  #Extracts numerical values from drive mode sensors by parsing command's output.
        try:
            mode_list.append(float(t))
        except ValueError:
            pass

    complete_data = []                                                          #Creates final data array.
    #complete_data.extend(headlightData)
    complete_data.extend(battery_list)                                          #Appends battery data into final array.
    complete_data.extend(crank_list)                                            #Appends crank data into final array.
    complete_data.extend(drive_list)                                            #Appends drive data into final array.
    complete_data.extend(mode_list)                                             #Appends driving mode data into final array.

    return complete_data                                                        #Returns complete data. Format: [battery, crank, drive, mode]

def set_light(flag):
    b = 0
    if flag :
        b = 1
    cmd = '{}/cmdHeadlight {}'.format(cmd_path, b)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, _ = p.communicate()

if __name__== "__main__":

    main_path = '/home/pi/Jett-Sen/hackbikeARICOM/'
    data_path = '/home/pi/Jett-Sen/hackbikeARICOM/jupyter_data/main_data/' #
    print("TerMITe Connecting....")

    num_tries = 5
    is_connected = False

    while not is_connected:
        try:
            TF = Termite_Access.termiteObject() # Find a termite
            is_connected = True
        except:
            print('couldn\'t connect to termite, retring after 5sec...')
            sleep(5)
            num_tries = num_tries - 1

            if num_tries < 0:
                sys.exit('Could not connect to a termite after few attempts')

    TF.activateCSV() #Swith terMITe output to CSV - Can choose JSON as well.

    print("Ready To Collect Data!")

    if not is_bluetooth:
        subprocess.call(['sudo python3 ' + main_path +  'data_indicator_light.py 1' , '-1'], shell=True)

    data_acquisition = False #Variable for activation and deactivation of data collection.

    while True: #Main loop.
        if (not data_acquisition) and data_activation(): #Check if headlight has been activated.
            data_acquisition = True
            datestring = str(datetime.datetime.now())
            datestring = datestring + ".txt"
            new_file = open(data_path + datestring,"w")                     #Create new file with data stamp name.
            if not is_bluetooth:
            	subprocess.call(['sudo python3 /home/pi/Jett-Sen/hackbikeARICOM/data_indicator_light.py 0' , '-1'], shell=True) #Turn indicator to RED.
            else :
                set_light(data_acquisition)
                
            print("Data Collection Enabeled")

        if data_acquisition and not data_activation(): #Check for sensor activation to shutdown data colection.
            data_acquisition = False
            new_file.close()                                                #Close file when collection is disabeled.
            if not is_bluetooth:
                subprocess.call(['sudo python3 /home/pi/Jett-Sen/hackbikeARICOM/data_indicator_light.py 1' , '-1'], shell=True) #Activate BLUE light on bike indicator.
            else:
                set_light(data_acquisition)
            print("Data Collection Diabeled")

        if data_acquisition == True:                                            #Enter if data collection is active.
            timestamp = str(datetime.datetime.now().time())                     #Gets Timestamp string.
            bikeData = str(getBikeData())                                       #Gets Complete Bike Sensor Data.
            bikeData = bikeData[1:-1]                                           #Formatting for taking out [] from data.
            print(timestamp[:11] + " , " + bikeData + " , " + TF.termiteValue)
            new_file.write(timestamp[:11] + "," + bikeData  + " , " + TF.termiteValue) #Write terMITe data with timestamp.
            time.sleep((1.0 / 1000) * 25)                                                     #Sampling at a rate of .5 s per data point.
