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
#from matplotlib.backends import _macosx

current_data_path = '/home/aricom/Desktop/Jett-Sen/panasonic_intelligence/'
file_name = 'Bike_data.txt'
destination_data_path = '/home/aricom/Desktop/Jett-Sen/panasonic_intelligence/clustered_data/'
new_file_name = 'clustered_' + file_name

current_data = np.genfromtxt(current_data_path + file_name , delimiter = ',',  dtype='str')
time_label = np.zeros(current_data.shape[0])

#Build new data structure including relevan variables for study. Each variable is normalized.
torque = current_data[:,[8]] #Minus one for Yasushi Data File
torque = torque.astype(np.float)
torque = ((torque - np.amin(torque)) / (np.amax(torque) - np.amin(torque)))

x_accel = current_data[:,[20]]
x_accel = x_accel.astype(np.float)
x_accel = ((x_accel - np.amin(x_accel)) / (np.amax(x_accel) - np.amin(x_accel)))

y_accel = current_data[:,[21]]
y_accel = y_accel.astype(np.float)
y_accel = ((y_accel - np.amin(y_accel)) / (np.amax(y_accel) - np.amin(y_accel)))


z_accel = current_data[:,[22]]
z_accel = z_accel.astype(np.float)
z_accel = ((z_accel - np.amin(z_accel)) / (np.amax(z_accel) - np.amin(z_accel)))

speed = current_data[:,[18]]
speed = speed.astype(np.float)
speed = ((speed - np.amin(speed)) / (np.amax(speed) - np.amin(speed)))

temp = current_data[:,[23]]
temp = temp.astype(np.float)
temp = ((temp - np.amin(temp)) / (np.amax(temp) - np.amin(temp)))

light = current_data[:,[24]]
light = light.astype(np.float)
light = ((light - np.amin(light)) / (np.amax(light) - np.amin(light)))

hum = current_data[:,[25]]
hum = hum.astype(np.float)
hum = ((hum - np.amin(hum)) / (np.amax(hum) - np.amin(hum)))

pressure = current_data[:,[27]]
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

plt.style.use('dark_background')

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlabel('Time')
ax.set_ylabel('Speed')
ax.set_zlabel('Torque')

#Run K means with n clusters.
kmeans = KMeans(n_clusters=5)
kmeans.fit(X)
y_kmeans = kmeans.predict(X) #This is the clustered vector.

centers = kmeans.cluster_centers_

#print (y_kmeans.shape)
#rint (X.shape)

output_data = np.column_stack([X, y_kmeans])
np.savetxt(destination_data_path + new_file_name, output_data, delimiter=',')

#print(output_data)

"""
#3D Plot to visualize relevant variables and classification of clusters within data file or bike trip.
img = ax.scatter3D(time_label, X[:, 3], X[:, 4], c=y_kmeans, cmap='viridis')
fig.colorbar(img)

plt.show()

#Plot each variable with respect to sequence of bike trip. (Time)
gs = gridspec.GridSpec(9,1)
fig = plt.figure()
dot_size = 16

ax = fig.add_subplot(gs[0])
ax.scatter(time_label,x_accel,c=y_kmeans, cmap='viridis', s = dot_size)
ax.set_ylabel(r'X', size =16)

ax = fig.add_subplot(gs[1])
ax.scatter(time_label,y_accel,c=y_kmeans, cmap='viridis', s = dot_size )
ax.set_ylabel(r'Y', size =16)
###ax.scatter3D(centers[:, 0], centers[:, 1], centers[:, 2], c='black', s=200, alpha=0.5);

ax = fig.add_subplot(gs[2])
ax.scatter(time_label,z_accel,c=y_kmeans, cmap='viridis', s = dot_size )
ax.set_ylabel(r'Z', size =16)

ax = fig.add_subplot(gs[3])
ax.scatter(time_label,speed,c=y_kmeans, cmap='viridis', s = dot_size)
ax.set_ylabel(r'S', size =16)

ax = fig.add_subplot(gs[4])
ax.scatter(time_label,torque,c=y_kmeans, cmap='viridis', s = dot_size)
ax.set_ylabel(r'To', size =16)

ax = fig.add_subplot(gs[5])
ax.scatter(time_label,temp,c=y_kmeans, cmap='viridis', s = dot_size)
ax.set_ylabel(r'T', size =16)

ax = fig.add_subplot(gs[6])
ax.scatter(time_label,light,c=y_kmeans, cmap='viridis', s = dot_size)
ax.set_ylabel(r'L', size =16)

ax = fig.add_subplot(gs[7])
ax.scatter(time_label,hum,c=y_kmeans, cmap='viridis', s = dot_size)
ax.set_ylabel(r'H', size =16)

ax = fig.add_subplot(gs[8])
ax.scatter(time_label,pressure,c=y_kmeans, cmap='viridis', s = dot_size)
ax.set_ylabel(r'P', size =16)

plt.show()

"""
