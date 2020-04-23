import numpy as np
import os

def combine(input, output, file_name):
    first = True
    for filename in os.listdir(input):
        if filename != '.DS_Store':
            if first:
                current_mat = np.genfromtxt(input + filename , delimiter = ',',  dtype='str')
                new_mat = current_mat
                first = False
            else:
                current_mat = np.genfromtxt(input + filename , delimiter = ',',  dtype='str')
                new_mat = np.vstack((new_mat, current_mat))
    np.savetxt(output + file_name , new_mat, delimiter = ',', fmt = '%s')


input = '/Users/AndresRico/Desktop/Jett-Sen/analysis/test_data/'
output = '/Users/AndresRico/Desktop/Jett-Sen/analysis/clustered_data/'
file = 'combined_jupyter.csv'

combine(input, output, file)
