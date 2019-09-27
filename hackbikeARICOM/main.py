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
#   This scriot can work in parallel with GPS and Camera data collection scripts (gps_main.py & camera.py)


import RPi.GPIO as GPIO                                                         #Import Library for GPIO Communication.
import Termite_Access                                                           #Used for communication with terMITe sensor.
import time
from time import sleep
import datetime                                                                 #Used for timestamps.
import subprocess                                                               #Activates subprocess calls.
import pigpio
import difflib

#Function for checking status of headlight for activation of data collection.
#Data collection is enabeled by turning on headlights.
def data_activation():
    path = '/home/pi/hackbikeARICOM/cmd'
    data_active = subprocess.check_output([ path + '/getHeadLight' , '-1'], shell=True) #Gets HeadLight Status (0 = OFF , 1 = ON)
    return float(data_active)                                                   #Returns float with headlight value.


#Function for extracting bike sensor data.
def getBikeData():
    path = '/home/pi/hackbikeARICOM/cmd'                                        #Specifies path for Panasonic Bike commands.

    #headlightData = subprocess.check_output([path + '/getHeadLight' , '-1'], shell=True)       #Uncomment if headlight data is desired. In this implementation it will always be 1 when recording.
    #headlightData = [float(headlightData[0])] #State of Headlight

    #print(headlightData)

    #Get Battery State Data.
    batteryData = subprocess.check_output([path + '/getBattery' , '-1'], shell=True) #Call to extract battery data.

    battery_list = []
    for t in batteryData.split():                                               #Extracts numerical values from battery sensors by parsing command's output.
        try:
            battery_list.append(float(t))
        except ValueError:
            pass

    #print(battery_list)

    #Get Crank State Data.
    crankData = subprocess.check_output([path + '/getCrank' , '-1'], shell=True)#Call to extract Crank data.

    crank_list = []
    for t in crankData.split():                                                 #Extracts numerical values from crank sensors by parsing command's output.
        try:
            crank_list.append(float(t))
        except ValueError:
                pass

    #print(crank_list)

    #Get Drive State Date.
    driveData = subprocess.check_output([path + '/getDrive' , '-1'], shell=True)#Call to extract Drive data.

    drive_list = []
    for t in driveData.split():                                                 #Extracts numerical values from drive sensors by parsing command's output.
        try:
            drive_list.append(float(t))
        except ValueError:
            pass

    #print(drive_list)

    #Get Mode State Data.
    modeData = subprocess.check_output([ path + '/getMode' , '-1'], shell=True) #Call to extract Driving Mode data.

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
                datestring = str(datetime.datetime.now())
                datestring = datestring + ".txt"
                new_file = open(data_path + datestring,"w")                     #Create new file with data stamp name.
                subprocess.call(['sudo python3 /home/pi/hackbikeARICOM/data_indicator_light.py 0' , '-1'], shell=True) #Turn indicator to RED.
                print("Data Collection Enabeled")

        if data_acquisition == True and data_activation() == 0: #Check for sensor activation to shutdown data colection.
                data_acquisition = False
                new_file.close()                                                #Close file when collection is disabeled.
                subprocess.call(['sudo python3 /home/pi/hackbikeARICOM/data_indicator_light.py 1' , '-1'], shell=True) #Activate BLUE light on bike indicator.
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
