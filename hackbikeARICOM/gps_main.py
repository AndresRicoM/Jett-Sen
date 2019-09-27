import sys
import pigpio
import difflib
import time
import subprocess
from time import sleep
import datetime

def getgps():

    RX=16

    try:
        pi = pigpio.pi()
        pi.set_mode(RX, pigpio.INPUT)
        pi.bb_serial_read_open(RX, 9600, 8)
    
        while  True : #1:
            (count, data) = pi.bb_serial_read(RX)
            #print data
            time.sleep(.5)
        
            if data[data.find("$GPGGA"):data.find("$GPGGA")+6] == '$GPGGA':
                msg = data[data.find("$GPGGA"):data.find("$GPGSA")]
                provlat = msg[msg.find("$GPGGA,")+17 : msg.find("$GPGGA")+27].decode("ascii", 'ignore')
                provlon = msg[msg.find("$GPGGA,")+30 : msg.find("$GPGGA")+41].decode("ascii", 'ignore')
                lat = provlat.encode('ascii', 'ignore')
                lon = provlon.encode('ascii', 'ignore')
                if lat[0] == "," or lat[0] == "9" :
                    #pi.bb_serial_read_close(RX)
                    #pi.stop()
                    return [-1,-1]
                else:
                    #pi.bb_serial_read_close(RX)
                    #pi.stop()
                    return [lat, lon]

    except:
        return [-2,-2]
    
    finally:
        pi.bb_serial_read_close(RX)
        pi.stop()
                

def data_activation():
    path = '/home/pi/hackbikeARICOM/cmd'
    data_active = subprocess.check_output([ path + '/getHeadLight' , '-1'], shell=True)
    return float(data_active)

        

if __name__== "__main__":
    
    main_path = '/home/pi/hackbikeARICOM/'
    data_path = '/home/pi/hackbikeARICOM/gps_data/'
    
    print 'GPS has been activated'
    
    print("Ready To Collect Data!")

    subprocess.call(['sudo python3 ' + main_path +  'data_indicator_light.py 2' , '-1'], shell=True)

    data_acquisition = False #Variable for activation and deactivation of data collection.

    while True: #Main loop.
        if data_acquisition == False and data_activation() == 1: #Check if touch sensor has been activated. 
                data_acquisition = True
                datestring = str(datetime.datetime.now())
                datestring = datestring + ".txt"
                new_file = open(data_path + datestring,"w")
                #subprocess.call(['sudo python3 /home/pi/hackbikeARICOM/data_indicator_light.py 0' , '-1'], shell=True)
                print("GPS Data Collection Enabeled")
                
        if data_acquisition == True and data_activation() == 0: #Check for sensor activation to shutdown data colection. 
                data_acquisition = False
                #time.sleep(.4)
                new_file.close()
                #subprocess.call(['sudo python3 /home/pi/hackbikeARICOM/data_indicator_light.py 1' , '-1'], shell=True)
                print("GPS Data Collection Diabeled")
                #time.sleep(2)
                
        if data_acquisition == True: #Enter if data collection is active.
            timestamp = str(datetime.datetime.now().time())
            gpsData = str(getgps())
            gpsData = gpsData[1:-1]
            gpsData = gpsData.replace("'", " ")
            print(timestamp[:11] + " , " + gpsData)
            new_file.write(timestamp[:11] + "," + gpsData)

    
