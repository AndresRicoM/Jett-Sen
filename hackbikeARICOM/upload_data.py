import os
import shutil
import urllib.request
import subprocess
import sys
from time import sleep

UP_DIR = '/opt/shared/bike_data/'
INTERVAL = 5 # secs

def check_internet():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False

def get_hostname():
    with open('/etc/hostname', 'r') as f:
        return f.read()

def upload_dir(directory):
    # abs path
    directory = os.path.abspath(directory);
    for root, dirs, files in os.walk(directory):
        for fn in files:
            upload_file(os.path.join(root, fn))
        for d in dirs:
            full_path = os.path.join(root, d);
            if not os.listdir(full_path):
                # dir is empty, remove the dir
                shutil.rmtree(full_path)
            else:
                upload_dir(os.path.join(root, d));

def upload_file(file_path):
    up_dir = os.path.join(UP_DIR, get_hostname())
    # scp /home/pi/hackbikeARICOM/neptune_data/main_data/2019-11-03 14:36:414660.txt eater:/opt/shared/bike_data/hackbike_neptune
    status = subprocess.call(['scp','{}'.format(file_path), 'eater:{}'.format(up_dir)], shell=True) 
    if status == 0:
        os.remove(file_path)

if __name__ == "__main__":
    target_dir = sys.argv[1]
    while True:
        if check_internet() :
            upload_dir(target_dir)
        sleep(5)
