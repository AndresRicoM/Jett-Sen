from subprocess import check_call
from os import path, remove, walk
from shutil import rmtree
from sys import argv
from socket import gethostbyname, create_connection
from time import sleep


REMOTE_SERVER = "www.google.com"
INTERVAL = 10

def is_connected(hostname):
    try:
        host = gethostbyname(hostname)
        s = create_connection((host, 80), 2)
        s.close()
        return True
    except:
        pass
    return False

destination = 'eater:/var/www/bike_data'

def clean_up_files(directory):
    for root, dirs, files in walk(directory):
        for d in dirs:
            clean_up_files(path.join(root, d))
        for f in files:
            remove(path.join(root, f))

def upload_dir(origin_dir, destination) :
    status_code = check_call('scp -r {} {}'.format(origin_dir, destination), shell = True)
    if(status_code == 0):
        # this cleans up the files
        clean_up_files(origin_dir)
        
if __name__ == '__main__':
    # run forever
    if is_connected(REMOTE_SERVER):
        origin_dir = path.abspath(argv[1])
        destination = argv[2]
        upload_dir(origin_dir, destination)

    sleep(INTERVAL)
        


