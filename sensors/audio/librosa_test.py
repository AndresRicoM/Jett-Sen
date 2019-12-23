import pandas as pd
import os
import librosa
import librosa.display
import struct
import IPython.display as ipd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.optimizers import Adam
from keras.utils import np_utils
from sklearn import metrics
import sklearn.preprocessing
#import LabelEncoder

from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

class WavFileHelper():

    def read_file_properties(self, filename):

        wave_file = open(filename,"rb")

        riff = wave_file.read(12)
        fmt = wave_file.read(36)

        num_channels_string = fmt[10:12]
        num_channels = struct.unpack('<H', num_channels_string)[0]

        sample_rate_string = fmt[12:16]
        sample_rate = struct.unpack("<I",sample_rate_string)[0]

        bit_depth_string = fmt[22:24]
        bit_depth = struct.unpack("<H",bit_depth_string)[0]

        return (num_channels, sample_rate, bit_depth)

def extract_features(file_name):

    try:
        audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast') 
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        mfccsscaled = np.mean(mfccs.T,axis=0)

    except Exception as e:
        print("Error encountered while parsing file: ", file)
        return None 

    return mfccsscaled

wavfilehelper = WavFileHelper()

metadata = pd.read_csv('/home/andres/Jett-Sen/hackbikeARICOM/audio/UrbanSound8K/metadata/UrbanSound8K.csv')

audiodata = []

features = []

for index, row in metadata.iterrows():

    file_name = os.path.join(os.path.abspath('/home/andres/Jett-Sen/hackbikeARICOM/audio/UrbanSound8K/audio'),'fold'+str(row["fold"])+'/',str(row["slice_file_name"]))
    data = wavfilehelper.read_file_properties(file_name)
    audiodata.append(data)
    class_label = row['classID']
    feature_data = extract_features(file_name)
    features.append([feature_data, class_label])

audiodf = pd.DataFrame(audiodata, columns=['num_channels','sample_rate','bit_depth'])
featuresdf = pd.DataFrame(features, columns = ['feature','class_label'])

print ('Feature extraction was successful for: ', len(featuresdf), 'files')
print (featuresdf)

print ('Number of channels distribution')
print (audiodf.num_channels.value_counts(normalize=True))

print ('Sample rates distribution')
print (audiodf.sample_rate.value_counts(normalize=True))

print ('Bit depth distribution')
print (audiodf.bit_depth.value_counts(normalize=True))

# Create X and Y inputs for classification.
X = np.array(featuresdf.feature.tolist())
y = np.array(featuresdf.class_label.tolist())

# Encode classification labels. 
#le = LabelEncoder()
#yy = to_categorical(le.fit_transform(y))

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

print ('Data Set was Processed Correctly')
