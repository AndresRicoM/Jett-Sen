import matplotlib
#matplotlib.use('GTK3Agg') #Uncomment when running program through SSH.

import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
import numpy as np
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec
from datetime import datetime
#from matplotlib.backends import _macosx

current_data_path = '/Users/AndresRico/Desktop/working/Jett-Sen/analysis/combined_data/'
file_name = 'combined_jupyter.csv' #'hackbike-jupyter-006f16e0-3235-11ea-9980-e166d58b4532.csv' #'combined_jupyter.csv'
destination_data_path = '/Users/AndresRico/Desktop/working/Jett-Sen/analysis/clustered_data/'
new_file_name = 'clustered_' + file_name

is_yasushi = True

#if is_yasushi:
#    current_data_path = '/home/yasushi/code/Jett-Sen/hackbikeARICOM/saturn_data/main_data/'
#    destination_data_path = '/home/yasushi/code/Jett-Sen/panasonic_intelligence/clustered_data/'

#file_name = '2019-11-11 09:03:37.293894.txt'

current_data = np.genfromtxt(current_data_path + file_name , delimiter = ',',  dtype='str')
time_label = np.zeros(current_data.shape[0])

#Build new data structure including relevant variables for study. Each variable is normalized.
"""
date_time = current_data[:,0]
for strings in range(date_time.shape[0]):
    holder_time = date_time[strings]
    date_time[strings] = datetime.strptime(holder_time, '%H:%M:%S.%f')
#date_time = date_time.astype(np.datetime64)
print (date_time)
"""

yasushi_data = -1 if is_yasushi else 0

torque = current_data[:,[8 + yasushi_data]] #Minus one for Yasushi Data File
torque = torque.astype(np.float)
torque = ((torque - np.amin(torque)) / (np.amax(torque) - np.amin(torque)))

x_accel = current_data[:,[20 + yasushi_data]]
x_accel = x_accel.astype(np.float)
x_accel = ((x_accel - np.amin(x_accel)) / (np.amax(x_accel) - np.amin(x_accel)))

y_accel = current_data[:,[21+ yasushi_data]]
y_accel = y_accel.astype(np.float)
y_accel = ((y_accel - np.amin(y_accel)) / (np.amax(y_accel) - np.amin(y_accel)))


z_accel = current_data[:,[22 + yasushi_data]]
z_accel = z_accel.astype(np.float)
z_accel = ((z_accel - np.amin(z_accel)) / (np.amax(z_accel) - np.amin(z_accel)))

speed = current_data[:,[18 + yasushi_data]]
speed = speed.astype(np.float)
speed = ((speed - np.amin(speed)) / (np.amax(speed) - np.amin(speed)))

temp = current_data[:,[23 + yasushi_data]]
temp = temp.astype(np.float)
temp = ((temp - np.amin(temp)) / (np.amax(temp) - np.amin(temp)))

light = current_data[:,[24 + yasushi_data]]
light = light.astype(np.float)
light = ((light - np.amin(light)) / (np.amax(light) - np.amin(light)))

hum = current_data[:,[25 + yasushi_data]]
hum = hum.astype(np.float)
hum = ((hum - np.amin(hum)) / (np.amax(hum) - np.amin(hum)))

pressure = current_data[:,[27 + yasushi_data ]]
pressure = pressure.astype(np.float)
pressure = ((pressure - np.amin(pressure)) / (np.amax(pressure) - np.amin(pressure)))

number = 0
for numbers in range(current_data.shape[0]):
    time_label[numbers] = number
    number = number + 1

X = np.hstack((x_accel,y_accel))
X = np.hstack((X,z_accel))
X = np.hstack((X,torque))
X = np.hstack((X,speed))
X = np.hstack((X,temp))
X = np.hstack((X,light))
X = np.hstack((X,hum))
X = np.hstack((X,pressure))

#plt.style.use('dark_background')

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlabel('Time')
ax.set_ylabel('Speed')
ax.set_zlabel('Torque')

#Run K means with n clusters.
kmeans = KMeans(n_clusters=7)
kmeans.fit(X)
y_kmeans = kmeans.predict(X) #This is the clustered vector.

centers = kmeans.cluster_centers_

#print (y_kmeans.shape)
#rint (X.shape)
#X = X.astype(np.str)
#y_kmeans = y_kmeans.astype(np.str)

output_data = np.column_stack([current_data[:,0], X])
output_data = np.column_stack([output_data, y_kmeans])
np.savetxt(destination_data_path + new_file_name, output_data, delimiter=',', fmt='%s')

plt.figure(figsize=(6, 6))
plt.scatter(time_label,x_accel,c=y_kmeans, cmap='plasma')
plt.title('X Acceleration Single Trip Clustering', fontsize=30)
#plt.xlabel(r'Time', fontsize=25)
#plt.ylabel('Acceleration', fontsize=25);

plt.show()
#print(output_data)

#3D Plot to visualize relevant variables and classification of clusters within data file or bike trip.
img = ax.scatter3D(time_label, X[:, 3], X[:, 4], c=y_kmeans, cmap='plasma') #viridis
fig.colorbar(img)

plt.show()

#Plot each variable with respect to sequence of bike trip. (Time)
gs = gridspec.GridSpec(9,1)
fig = plt.figure()
plt.title('Multiple Trip Fusion Data Clustering', fontsize=30)
#plt.ylabel('Normalized Fusion Variables', fontsize=25)
#plt.xlabel('Time', fontsize=25)
plt.xticks([])
plt.yticks([])
dot_size = 16

ax = fig.add_subplot(gs[0])
ax.scatter(time_label,x_accel,c=y_kmeans, cmap='plasma', s = dot_size)
ax.set_ylabel(r'X-Acc', size =15)
ax.set_yticklabels([])
ax.set_xticklabels([])

ax = fig.add_subplot(gs[1])
ax.scatter(time_label,y_accel,c=y_kmeans, cmap='plasma', s = dot_size )
ax.set_ylabel(r'Y-Acc', size =15)
ax.set_yticklabels([])
ax.set_xticklabels([])
###ax.scatter3D(centers[:, 0], centers[:, 1], centers[:, 2], c='black', s=200, alpha=0.5);

ax = fig.add_subplot(gs[2])
ax.scatter(time_label,z_accel,c=y_kmeans, cmap='plasma', s = dot_size )
ax.set_ylabel(r'Z-Acc', size =15)
ax.set_yticklabels([])
ax.set_xticklabels([])

ax = fig.add_subplot(gs[3])
ax.scatter(time_label,speed,c=y_kmeans, cmap='plasma', s = dot_size)
ax.set_ylabel(r'Speed', size =15)
ax.set_yticklabels([])
ax.set_xticklabels([])

ax = fig.add_subplot(gs[4])
ax.scatter(time_label,torque,c=y_kmeans, cmap='plasma', s = dot_size)
ax.set_ylabel(r'Torq', size =15)
ax.set_yticklabels([])
ax.set_xticklabels([])

ax = fig.add_subplot(gs[5])
ax.scatter(time_label,temp,c=y_kmeans, cmap='plasma', s = dot_size)
ax.set_ylabel(r'Temp', size =15)
ax.set_yticklabels([])
ax.set_xticklabels([])

ax = fig.add_subplot(gs[6])
ax.scatter(time_label,light,c=y_kmeans, cmap='plasma', s = dot_size)
ax.set_ylabel(r'Light', size =15)
ax.set_yticklabels([])
ax.set_xticklabels([])

ax = fig.add_subplot(gs[7])
ax.scatter(time_label,hum,c=y_kmeans, cmap='plasma', s = dot_size)
ax.set_ylabel(r'Hum', size =15)
ax.set_yticklabels([])
ax.set_xticklabels([])

ax = fig.add_subplot(gs[8])
ax.scatter(time_label,pressure,c=y_kmeans, cmap='plasma', s = dot_size)
ax.set_ylabel(r'Press', size =15)
ax.set_xlabel(r'Time Sequenced Trips', size =15)
ax.set_yticklabels([])
ax.set_xticklabels([])

plt.show()
