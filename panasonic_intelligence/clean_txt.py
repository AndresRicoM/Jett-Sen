# cleans the txt produced by main.py

# issue
# some bikes record data differently, due to termites not change mode to CSV_MODE
# this script converts it to the right csv file and overwrites it. it does not change anything if it's already fine.

import re
import sys
import os

def convert_to_csv(file_path):

    # make sure it's absolute
    path = os.path.abspath(file_path)

    print('checking: {}'.format(path))

    # 1. read the file
    with open(path, 'r') as f:
        # 2. read line
        data = f.read()
        
    # 3. regex the unwanted strings, replace them
    new_data = re.sub(r" ,  X \= ", ", ", data)
    new_data = re.sub(r" Y \=| Z \=| Temp \=| Light \=| Humidity \=| Proximity \=| Pressure \=| Altitude \=| DewPoint \=", ",", new_data)
    
    ## 4. overwrite them
    
    # 5. save in the same file
    with open(path, 'w') as f:
         f.write(new_data)

    print('done: {}'.format(path))


# make sure its absolute path
rel_path = sys.argv[1]
path = os.path.abspath(rel_path)

if os.path.isfile(path):
    convert_to_csv(path)
else:
    (_, _, filenames) = os.walk(path).next()
    [convert_to_csv(os.path.join(path, f)) for f in filenames]


print('done.')