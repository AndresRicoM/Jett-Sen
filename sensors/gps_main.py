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
#   Main script for collecting data from GPS Module.
#   A Raspberry Pi Camera Module is used in this implementation.
#
#   This script can work in parallel with Bike/terMITe and GPS data collection scripts (gps_main.py & camera.py)

import sys
import pigpio                                                                   #Library for managing TX/RX communication on I/O pins in Raspberry Pi 3+
import difflib
import time
import subprocess
from time import sleep
import datetime                                                                 #Import for timestamping GPS data for later processing and combination of data.

#Function for accesing GPS data through virtual serial communication.
#GPS will constantly transmit received data.
def getgps():

    RX=16                                                                       #Define pin 16 on Raspberry Pi as virtual RX pin.

    try:
        pi = pigpio.pi()
        pi.set_mode(RX, pigpio.INPUT)                                           #Define RX pin as an INPUT pin.
        pi.bb_serial_read_open(RX, 9600, 8)                                     #Open serial at 9600 Baud rate.

        while  True : #1:
            (count, data) = pi.bb_serial_read(RX)                               #Receive Data.
            #print data
            time.sleep(.5)                                                      #Delay for stability of communication protocol.

            if data[data.find("$GPGGA"):data.find("$GPGGA")+6] == '$GPGGA':     #Parse NMEA data.
                msg = data[data.find("$GPGGA"):data.find("$GPGSA")]             #Access only GPGGA data.
                provlat = msg[msg.find("$GPGGA,")+17 : msg.find("$GPGGA")+27].decode("ascii", 'ignore')     #Parse latitude data.
                provlon = msg[msg.find("$GPGGA,")+30 : msg.find("$GPGGA")+41].decode("ascii", 'ignore')     #Parse longitude data.
                lat = provlat.encode('ascii', 'ignore')                         #Encode data into ascii format.
                lon = provlon.encode('ascii', 'ignore')                         #Encode data into ascii format.
                if lat[0] == "," or lat[0] == "9" :
                    return [-1,-1]                                              #Return negative 1 coordinates id data was received with errors or with no sufficient decimal numbers of presicion.
                else:
                    return [lat, lon]                                           #Return lat and lon values if they were received correctly.

    except:
        return [-2,-2]                                                          #Return negative 2 if communication with GPS module failed.

    finally:
        pi.bb_serial_read_close(RX)                                             #Close virtual serial communication to avoid affecting other data collection processes.
        pi.stop()


#Function for checking status of headlight for activation of data collection.
#Data collection is enabeled by turning on headlights.
def data_activation():
    path = '/home/pi/Jett-Sen/hackbikeARICOM/cmd'
    data_active = subprocess.check_output([ path + '/getHeadLight' , '-1'], shell=True) #Gets HeadLight Status (0 = OFF , 1 = ON)
    return float(data_active)                                                   #Returns float with headlight value.



if __name__== "__main__":

    main_path = '/home/pi/Jett-Sen/hackbikeARICOM/'                                      #Declare main path for scripts.
    data_path = '/home/pi/Jett-Sen/hackbikeARICOM/gps_data/'                             #Declare path for storing data files.

    print 'GPS has been activated'

    print("Ready To Collect Data!")

    subprocess.call(['sudo python3 ' + main_path +  'data_indicator_light.py 2' , '-1'], shell=True) #Turn light green when GPS has been activated.

    data_acquisition = False #Variable for activation and deactivation of data collection.

    while True: #Main loop for data collection.
        if data_acquisition == False and data_activation() == 1: #Check if headlight has been activated.
                data_acquisition = True
                datestring = str(datetime.datetime.now())
                datestring = datestring + ".txt"
                new_file = open(data_path + datestring,"w")                     #Open file with timestamp name when data collection has beeen enabeled.
                print("GPS Data Collection Enabeled")

        if data_acquisition == True and data_activation() == 0: #Check for headlight deactivation to shutdown data colection.
                data_acquisition = False
                new_file.close()
                print("GPS Data Collection Diabeled")                           #Close file when collection is disabeled.
                #time.sleep(2)

        if data_acquisition == True: #Enter if data collection is active.
            timestamp = str(datetime.datetime.now().time())                     #Create time stamp string.
            gpsData = str(getgps())                                             #String gps data.
            gpsData = gpsData[1:-1]                                             #Format GPS data by taking [] out.
            gpsData = gpsData.replace("'", " ")
            print(timestamp[:11] + " , " + gpsData)
            new_file.write(timestamp[:11] + "," + gpsData +  "\n")              #Write data into file.
