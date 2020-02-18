# -*- coding: UTF-8 -*-

#
#      ██╗███████╗████████╗████████╗   ███████╗███████╗███╗   ██╗
#      ██║██╔════╝╚══██╔══╝╚══██╔══╝   ██╔════╝██╔════╝████╗  ██║
#      ██║█████╗     ██║      ██║█████╗███████╗█████╗  ██╔██╗ ██║
# ██   ██║██╔══╝     ██║      ██║╚════╝╚════██║██╔══╝  ██║╚██╗██║
# ╚█████╔╝███████╗   ██║      ██║      ███████║███████╗██║ ╚████║
#  ╚════╝ ╚══════╝   ╚═╝      ╚═╝      ╚══════╝╚══════╝╚═╝  ╚═══╝
#
#   Sensorized Panasonic Jetter Hackable Bike

#Function for obtaining a UUID to assign to each trip.
#The function created a UUID, and checks that it has never created it with a data folder containig all UUIDs created in the past.
#The function returns UUID along with hostname tag for bikes to create new files. 

import uuid
import socket
#print(socket.gethostname())


def get_uuid():
    
    path = '/home/pi/Jett-Sen/sensors/UUID/'
    file_name = 'generated_uuids.txt'

    is_unique = True
    new_id = uuid.uuid1()
    #print (new_id)

    uuid_file = open(path + file_name,"r")

    for lines in uuid_file:
        if lines == new_id :
            is_unique = False
            print('WARNING: UUID is a duplicate!')

    if is_unique:
        uuid_file = open(path + file_name,"a")
        uuid_file.write(str(new_id) + '\n')
        uuid_file.close()
        return (str(socket.gethostname()) + '-' + str(new_id))
        print('Succesfully Assigned UUID')
    else:
        get_uuid()

#print(get_uuid())
