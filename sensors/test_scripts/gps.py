
import sys
import pigpio
import difflib
import time
import subprocess
    

def getgps():

    RX=16

    try:
        pi = pigpio.pi()
        pi.set_mode(RX, pigpio.INPUT)
        pi.bb_serial_read_open(RX, 9600, 8)
    
        while True: # 1:
            (count, data) = pi.bb_serial_read(RX)
            #print data
            time.sleep(.5)
            #print  data
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

#getgps()
while True:
	print getgps()
