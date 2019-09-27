# ! /usr/bin/python
# coding=utf-8
#******************************************************************************/

#  ████████╗███████╗██████╗ ███╗   ███╗██╗████████╗███████╗███████╗     \         /
#  ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║╚══██╔══╝██╔════╝██╔════╝      `-.`-'.-'
#     ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║   █████╗  ███████╗      ,:--.--:.
#     ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║   ██╔══╝  ╚════██║     / |  |  | \
#     ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║   ██║   ███████╗███████║      /\  |  /\
#     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝   ╚═╝   ╚══════╝╚══════╝      | `.:.' |

#Carson Smuts - MIT 2019
#******************************************************************************/


#TerMITe_Seeker : Carson Smuts
# WRITTEN FOR HACK A BIKE Project


#
#A simple class to seek out, connect, and read from TerMITes.
#All computation, control and encoding is done on the termite hardware.
#This simple open a USB port to the hardware and listens to messages coming through.
#
#Added options for JSON formatting
#

import sys
import glob
import time
from time import sleep

import serial
from serial import SerialException
from serial.tools import list_ports

import socket

from threading import Thread

UDP_IP = "127.0.0.1"
UDP_PORT = 7777
termiteAddress = ""
termitePort = serial.Serial()

enableUDP = False


class termiteObject(object):
    termiteValue = "-1"
    def __init__(self):

        try:
            termiteAddress = findTermite()
            global termitePort
            termitePort = serial.Serial(termiteAddress, 115200)
            thread = Thread(target=self.termiteRunner, args=())
            thread.daemon = True  # Daemonize
            thread.start()
        except SerialException:
            print ("Could not start SliderScope.... port already open.... or not found.... check with Carson")


    def activateJSON(self):
        termitePort.write(str.encode("CMD\r\n"))
        sleep(0.5)
        termitePort.write(str.encode("JSON\r\n"))
        sleep(0.5)

        while termitePort.in_waiting:
            for c in termitePort.read():
                if c == "\n":
                    break
        print("JSON output has been activated!")

        termitePort.write(str.encode("EXT\r\n"))
        sleep(0.5)
        
    def activateCSV(self):
        termitePort.write(str.encode("CMD\r\n"))
        sleep(0.5)
        termitePort.write(str.encode("CSV\r\n"))
        sleep(0.5)

        while termitePort.in_waiting:
            for c in termitePort.read():
                if c == "\n":
                    break
        print("CSV output has been activated!")

        termitePort.write(str.encode("EXT\r\n"))
        sleep(0.5)


    def termiteRunner(self):
        while True:
            #print "running"
            try:
                termitePort.reset_input_buffer()
                #sliderScopePort.flush()
                #time.sleep(.1)
                x = termitePort.readline()

                if x:

                    if (enableUDP):
                        sock = socket.socket(socket.AF_INET,  # Internet
                        socket.SOCK_DGRAM)  # UDP
                        sock.sendto(x, (UDP_IP, UDP_PORT))
                    #return x
                    self.termiteValue = x


            except SerialException:
                print ("SliderScope unavailable.... check with Carson")
                #return -1
                self.termiteValue = -1



def findTermite():
    termiteAddress = ""
    VID = "10C4"
    PID = "EA60"

    device_list = list_ports.comports()
    for device in device_list:
        if (device.vid != None or device.pid != None):
            if ("{:04X}".format(device.vid) == VID and "{:04X}".format(device.pid) == PID):
                port = device.device

                print("TMT: Looking for TerMITe Port....")

                try:
                    s = serial.Serial(port, 115200, timeout=10)

                    s.write(str.encode("CMD\r\n"))
                    sleep(1.0)

                    line = []
                    lines = []

                    while s.in_waiting:
                        for c in s.read():
                            line.append(c)
                            if c == "\n":
                                lineOut = ''.join(line)
                                # print("Line: " + ''.join(line))
                                lines.append(lineOut)

                                line = []

                                break

                    s.write(str.encode("TMT\r\n"))
                    sleep(0.5)

                    while s.in_waiting:
                        for c in s.read():
                            line.append(c)
                            if c == "\n":
                                lineOut = ''.join(line)
                                # print("Line: " + ''.join(line))
                                lines.append(lineOut)

                                line = []

                                break

                    result = lines[len(lines) - 1]
                    print(result)

                    if result == "+TERMITE VERSION:1.00\r\n":
                        print("TMT: Found Termite")
                        s.write(str.encode("EXT\r\n"))
                        sleep(0.5)
                        termiteAddress = port
                    s.close()


                except (OSError, serial.SerialException):
                    pass
                return termiteAddress
                break



            #Do NOT use this function..... for testing only
def serial_ports():
        if sys.platform.startswith("win"):
            ports = ["COM%s" % (i + 1) for i in range(256)]
        elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
            ports = glob.glob("/dev/tty[A-Za-z]*")
        elif sys.platform.startswith("darwin"):
            ports = glob.glob("/dev/tty.*")
        else:
            raise EnvironmentError("Unsupported platform")

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.write(str.encode("CMD"))
                sleep(0.5)
                readX = s.readline()
                print(readX)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result



