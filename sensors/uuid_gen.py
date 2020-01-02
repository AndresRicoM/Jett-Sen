import uuid

path = '/home/pi/Jett-Sen/sensors/UUID/'
file_name = 'generated_uuids.txt'

is_unique = False
new_id = uuid.uuid1()
print (new_id)

while not is_unique:
    print('Looking =) ...')
    
uuid_file = open(data_path + datestring,"r")

uuid_file = open(data_path + datestring,"w")