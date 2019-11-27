import pandas as pd
import os
import librosa
import librosa.display
import struct

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

wavfilehelper = WavFileHelper()

audiodata = []
for index, row in metadata.iterrows():
	file_name = os.path.join(os.path.abspath('/UrbanSound8K/audio/'),'fold'+str(row["fold"])+'/',str(row["slice_file_name"]))
	data = wavfilehelper.read_file_properties(file_name)
	audiodata.append(data)

audiodf = pd.DataFrame(audiodata, columns=['num_channels','sample_rate','bit_depth'])
