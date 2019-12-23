import RPi.GPIO as GPIO #Import Library for GPIO Communication.
import time
import Termite_Access
import time
from time import sleep
import datetime
import subprocess
import pigpio
import difflib

def getgps():

    RX=16

    try:
        pi = pigpio.pi()
        pi.set_mode(RX, pigpio.INPUT)
        pi.bb_serial_read_open(RX, 9600, 8)
    
        while 1:
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
    data_active = subprocess.check_output(['/home/pi/hackbikeARICOM/getHeadLight' , '-1'], shell=True)
    return float(data_active)

def getBikeData():
    headlightData = subprocess.check_output(['/home/pi/hackbikeARICOM/getHeadLight' , '-1'], shell=True)
    headlightData = [float(headlightData[0])] #State of Headlight

    #print(headlightData)

    #Get Battery State Data. 
    batteryData = subprocess.check_output(['/home/pi/hackbikeARICOM/getBattery' , '-1'], shell=True)

    battery_list = []
    for t in batteryData.split():
        try:
            battery_list.append(float(t))
        except ValueError:
            pass
    
    #print(battery_list)

    #Get Crank State Data. 
    crankData = subprocess.check_output(['/home/pi/hackbikeARICOM/getCrank' , '-1'], shell=True)

    crank_list = []
    for t in crankData.split():
        try:
            crank_list.append(float(t))
        except ValueError:
                pass
    
    #print(crank_list)

    #Get Drive State Date. 
    driveData = subprocess.check_output(['/home/pi/hackbikeARICOM/getDrive' , '-1'], shell=True)

    drive_list = []
    for t in driveData.split():
        try:
            drive_list.append(float(t))
        except ValueError:
            pass
    
    #print(drive_list)

    #Get Mode State Data.
    modeData = subprocess.check_output(['/home/pi/hackbikeARICOM/getMode' , '-1'], shell=True)

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
    
    print("TerMITe Connecting....")
    TF = Termite_Access.termiteObject() #Find a terMITe.
    TF.activateCSV() #Swith terMITe output to CSV - Can choose JSON as well.
    print("First terMITe was found")
    print("CSV has been activated")
    #TR = Termite_Access.termiteObject()
    #print("Second terMITe was found")
    print("Ready To Collect Data!")

    subprocess.call(['sudo python3 /home/pi/hackbikeARICOM/data_indicator_light.py 1' , '-1'], shell=True)

#    GPIO.setwarnings(False) #Warnings not activated.
#    GPIO.setmode(GPIO.BOARD) #Uses board numbers to reference GPIO Pins. 
#    GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Set pin 7 to read. 


    data_acquisition = False #Variable for activation and deactivation of data collection.
    gps_lock = False
    
    #while not gps_lock:
    #    gps_locking = subprocess.check_output(['python /home/pi/hackbikeARICOM/gps.py' , '-1'], shell=True)
    #    print gps_locking
    #    #print type(gps_locking)
    #    if gps_locking[1] != '-':
    #        gps_lock = True
    #        print 'GPS is locked and ready!'

    while True: #Main loop.
        if data_acquisition == False and data_activation() == 1: #Check if touch sensor has been activated. 
                data_acquisition = True
                #time.sleep(.4)
                datestring = str(datetime.datetime.now())
                datestring = datestring + ".txt"
                new_file = open('/home/pi/hackbikeARICOM/data/' + datestring,"w")
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
            gpsData = str(getgps())
            gpsData = gpsData[1:-1]
            gpsData = gpsData.replace("'", " ")
            #print gpsData
            #gpsData = gpsData[:-1]
            print(timestamp[:11] + " , " + gpsData + " , " + bikeData + " , " + TF.termiteValue)
            new_file.write(timestamp[:11] + "," + gpsData + "," + bikeData  + " , " + TF.termiteValue) #Write terMITe data with timestamp.
            #print(TR.termiteValue)
            time.sleep(0.1)
 
