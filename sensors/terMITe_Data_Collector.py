import RPi.GPIO as GPIO #Import Library for GPIO Communication.
import time
import Termite_Access
import time
from time import sleep
import datetime
import subprocess

print("TerMITe Connecting....")
TF = Termite_Access.termiteObject() #Find a terMITe.
TF.activateCSV() #Swith terMITe output to CSV - Can choose JSON as well.
print("First terMITe was found")
#TR = Termite_Access.termiteObject()
#print("Second terMITe was found")
print("Ready To Collect Data!")

subprocess.call(['sudo python3 data_indicator_light.py 0' , '-1'], shell=True)

GPIO.setwarnings(False) #Warnings not activated.
GPIO.setmode(GPIO.BOARD) #Uses board numbers to reference GPIO Pins. 
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Set pin 7 to read. 


data_acquisition = False #Variable for activation and deactivation of data collection. 

while True: #Main loop.
    if data_acquisition == False and GPIO.input(7) == GPIO.HIGH: #Check if touch sensor has been activated. 
            data_acquisition = True
            time.sleep(.4)
            datestring = str(datetime.datetime.now())
            datestring = datestring + ".txt"
            new_file = open(datestring,"w")
            subprocess.call(['sudo python3 data_indicator_light.py 1' , '-1'], shell=True)
            print("Data Collection Enabeled")
            
    if data_acquisition == True and GPIO.input(7) == GPIO.HIGH: #Check for sensor activation to shutdown data colection. 
            data_acquisition = False
            time.sleep(.4)
            new_file.close()
            subprocess.call(['sudo python3 data_indicator_light.py 0' , '-1'], shell=True)
            print("Data Collection Diabeled")
            
    if data_acquisition == True: #Enter if data collection is active.
        timestamp = str(datetime.datetime.now().time())
        new_file.write(timestamp[:11] + ", " + TF.termiteValue) #Write terMITe data with timestamp.
        print(TF.termiteValue)
        #print(TR.termiteValue)
        time.sleep(0.1)
        