import subprocess
import sys
import os
import time
import signal
from uuid_gen import get_uuid

path = '/home/pi/Jett-Sen/sensors/'
is_bluetooth = False

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
        path = '/home/pi/Jett-Sen/sensors/cmd'
        data_active = subprocess.check_output([ path + '/getHeadLight' , '-1'], shell=True) #Gets HeadLight Status (0 = OFF , $
        #Returns float with headlight value.
        return  int(data_active) == 1

if __name__ == '__main__':

	is_bluetooth = False
	data_acquisition = False #Variable for activation and deactivation of data collection.
	#record_audio(*sys.argv[1:])
	main_path = '/home/pi/Jett-Sen/sensors/'
	data_path = '/home/pi/Jett-Sen/sensors/data/audio_data/' #Change last two lines depending on the bike running the program.

	while True: #Main loop.

		if (not data_acquisition) and data_activation(): #Check if headlight has been activated.
			data_acquisition = True
			uuid_name = get_uuid()
			uuid_name = uuid_name + ".wav"
			proc_args = ['arecord', '-D' , 'hw:1,0' , '-f' , 'cd' ,data_path + uuid_name , '-c' , '2']
			rec_proc = subprocess.Popen(proc_args, shell=False, preexec_fn=os.setsid)

            		#new_file = open(data_path + uuid_name,"w")                     #Create new file with data stamp name.
		#if not is_bluetooth:
			#subprocess.call(['sudo python3 /home/pi/Jett-Sen/sensors/data_indicator_light.py 0' , '-1'], shell=True) #Turn indicator to RED.
		#else :
			#set_light(data_acquisition)

			print("Recording Audio")

		if data_acquisition and not data_activation(): #Check for sensor activation to shutdown data colection.
			data_acquisition = False
			os.killpg(rec_proc.pid, signal.SIGTERM)
			rec_proc.terminate()
			rec_proc = None                                                #Close file when collection is disabeled.
		#if not is_bluetooth:
			#subprocess.call(['sudo python3 /home/pi/Jett-Sen/sensors/data_indicator_light.py 1' , '-1'], shell=True) #Activate BLUE light on bike indicator.
		#else:
			#set_light(data_acquisition)

			print("Data Collection Diabeled")
