import sys
import RPi.GPIO as GPIO                                                         #Import Library for GPIO Communication.
import Termite_Access                                                           #Used for communication with terMITe sensor.
import time
from time import sleep
import datetime                                                                 #Used for timestamps.
import subprocess                                                               #Activates subprocess calls.
import pigpio
import difflib
import json

def cmd_path():
    return '/home/pi/hackbicycle/cmd'

#Function for checking status of headlight for activation of data collection.
#Data collection is enabeled by bluetooth communication.
def data_activation():
    status_json_path = '/home/pi/status.json'
    is_recording = False
    with open(status_json_path, 'r') as f:
        try:
            status = json.load(f)
	    is_recording = status['record']
        except ValueError:
            print("could not parse json data")
            pass
            

    return is_recording                                                   #Returns float with headlight value.


#Function for extracting bike sensor data.
def getBikeData():

    #Get Battery State Data.
    batteryData = subprocess.check_output([cmd_path() + '/getBattery' , '-1'], shell=True) #Call to extract battery data.

    battery_list = []
    for t in batteryData.split():                                               #Extracts numerical values from battery sensors by parsing command's output.
        try:
            battery_list.append(float(t))
        except ValueError:
            pass

    #print(battery_list)

    #Get Crank State Data.
    crankData = subprocess.check_output([cmd_path() + '/getCrank' , '-1'], shell=True)#Call to extract Crank data.

    crank_list = []
    for t in crankData.split():                                                 #Extracts numerical values from crank sensors by parsing command's output.
        try:
            crank_list.append(float(t))
        except ValueError:
                pass

    #print(crank_list)

    #Get Drive State Date.
    driveData = subprocess.check_output([cmd_path() + '/getDrive' , '-1'], shell=True)#Call to extract Drive data.

    drive_list = []
    for t in driveData.split():                                                 #Extracts numerical values from drive sensors by parsing command's output.
        try:
            drive_list.append(float(t))
        except ValueError:
            pass

    #print(drive_list)

    #Get Mode State Data.
    modeData = subprocess.check_output([cmd_path() + '/getMode' , '-1'], shell=True) #Call to extract Driving Mode data.

    mode_list = []
    for t in modeData.split():                                                  #Extracts numerical values from drive mode sensors by parsing command's output.
        try:
            mode_list.append(float(t))
        except ValueError:
            pass

    complete_data = []                                                          #Creates final data array.
    complete_data.extend(battery_list)                                          #Appends battery data into final array.
    complete_data.extend(crank_list)                                            #Appends crank data into final array.
    complete_data.extend(drive_list)                                            #Appends drive data into final array.
    complete_data.extend(mode_list)                                             #Appends driving mode data into final array.

    return complete_data                                                        #Returns complete data. Format: [battery, crank, drive, mode]

def set_light(flag):
    b = 0
    if flag :
        b = 1
    cmd = '{}/cmdHeadlight {}'.format(cmd_path(), b)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, _ = p.communicate()


if __name__== "__main__":

    main_path = '/home/pi/Jett-Sen/hackbikeARICOM/'
    data_path = '/home/pi/Jett-Sen/hackbikeARICOM/data/'
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

    # subprocess.call(['sudo python3 ' + main_path +  'data_indicator_light.py 1' , '-1'], shell=True)

    data_acquisition = False #Variable for activation and deactivation of data collection.

    while True: #Main loop.
        if (not data_acquisition) and data_activation(): #Check if headlight has been activated.
            data_acquisition = True
            datestring = str(datetime.datetime.now())
            datestring = datestring + ".txt"
            new_file = open(data_path + datestring,"w")                     #Create new file with data stamp name.
            set_light(data_acquisition)
            # subprocess.call(['sudo python3 /home/pi/hackbikeARICOM/data_indicator_light.py 0' , '-1'], shell=True) #Turn indicator to RED.
                
            print("Data Collection Enabeled")

        if data_acquisition and not data_activation(): #Check for sensor activation to shutdown data colection.
            data_acquisition = False
            new_file.close()                                                #Close file when collection is disabeled.
            # subprocess.call(['sudo python3 /home/pi/hackbikeARICOM/data_indicator_light.py 1' , '-1'], shell=True) #Activate BLUE light on bike indicator.
            set_light(data_acquisition)
            print("Data Collection Diabeled")
            #time.sleep(2)

        if data_acquisition == True:                                            #Enter if data collection is active.
            timestamp = str(datetime.datetime.now().time())                     #Gets Timestamp string.
            bikeData = str(getBikeData())                                       #Gets Complete Bike Sensor Data.
            bikeData = bikeData[1:-1]                                           #Formatting for taking out [] from data.
            print(timestamp[:11] + " , " + bikeData + " , " + TF.termiteValue)
            new_file.write(timestamp[:11] + "," + bikeData  + " , " + TF.termiteValue) #Write terMITe data with timestamp.
            #print(TR.termiteValue)
            time.sleep(0.4)                                                     #Sampling at a rate of .5 s per data point.
