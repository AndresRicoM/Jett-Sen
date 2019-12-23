import subprocess

while True:
    
    #Get Headlight State Data.
    headlightData = subprocess.check_output(['./getHeadLight' , '-1'], shell=True)
    headlightData = [float(headlightData[0])] #State of Headlight

    #print(headlightData)

    #Get Battery State Data. 
    batteryData = subprocess.check_output(['./getBattery' , '-1'], shell=True)

    battery_list = []
    for t in batteryData.split():
        try:
            battery_list.append(float(t))
        except ValueError:
            pass
    
    #print(battery_list)

    #Get Crank State Data. 
    crankData = subprocess.check_output(['./getCrank' , '-1'], shell=True)

    crank_list = []
    for t in crankData.split():
        try:
            crank_list.append(float(t))
        except ValueError:
                pass
    
    #print(crank_list)

    #Get Drive State Date. 
    driveData = subprocess.check_output(['./getDrive' , '-1'], shell=True)

    drive_list = []
    for t in driveData.split():
        try:
            drive_list.append(float(t))
        except ValueError:
            pass
    
    #print(drive_list)

    #Get Mode State Data.
    modeData = subprocess.check_output(['./getMode' , '-1'], shell=True)

    mode_list = []
    for t in modeData.split():
        try:
            mode_list.append(float(t))
        except ValueError:
            pass
    
    #print(mode_list)

    complete_data = []
    complete_data.extend(headlightData)
    complete_data.extend(battery_list)
    complete_data.extend(crank_list)
    complete_data.extend(drive_list)
    complete_data.extend(mode_list)

    print(str(complete_data))



