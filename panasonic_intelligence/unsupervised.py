import matplotlib
matplotlib.use('GTK3Agg')

import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
import numpy as np
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec
#from matplotlib.backends import _macosx

#X, y_true = make_blobs(n_samples=300, centers=4,
#                       cluster_std=0.60, random_state=0)
current_data = np.genfromtxt('/home/andres/panasonic_intelligence/Bike_data.txt', delimiter = ',',  dtype='str')
time_label = np.zeros(current_data.shape[0])
#time_label

print (current_data.shape)
print (time_label.shape)

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

print (time_label)

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
#ax.scatter3D(X[:, 0], X[:, 1],X[:, 2] , s=50);

"""
sse = []
list_k = list(range(1, 11))


for i, k in enumerate([2, 3, 4, 6, 8, 10]):
    #km = KMeans(n_clusters=k)
    #km.fit(X)
    #sse.append(km.inertia_)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(18, 7)

    # Run the Kmeans algorithm
    km = KMeans(n_clusters=k)
    labels = km.fit_predict(X)
    centroids = km.cluster_centers_

    # Get silhouette samples
    silhouette_vals = silhouette_samples(X, labels)

    # Silhouette plot
    y_ticks = []
    y_lower, y_upper = 0, 0
    for i, cluster in enumerate(np.unique(labels)):
        cluster_silhouette_vals = silhouette_vals[labels == cluster]
        cluster_silhouette_vals.sort()
        y_upper += len(cluster_silhouette_vals)
        ax1.barh(range(y_lower, y_upper), cluster_silhouette_vals, edgecolor='none', height=1)
        ax1.text(-0.03, (y_lower + y_upper) / 2, str(i + 1))
        y_lower += len(cluster_silhouette_vals)

    # Get the average silhouette score and plot it
    avg_score = np.mean(silhouette_vals)
    ax1.axvline(avg_score, linestyle='--', linewidth=2, color='green')
    ax1.set_yticks([])
    ax1.set_xlim([-0.1, 1])
    ax1.set_xlabel('Silhouette coefficient values')
    ax1.set_ylabel('Cluster labels')
    ax1.set_title('Silhouette plot for the various clusters', y=1.02);

    # Scatter plot of data colored with labels
    ax2.scatter(X[:, 0], X[:, 1], c=labels)
    ax2.scatter(centroids[:, 0], centroids[:, 1], marker='*', c='r', s=250)
    ax2.set_xlim([-2, 2])
    ax2.set_xlim([-2, 2])
    ax2.set_xlabel('Eruption time in mins')
    ax2.set_ylabel('Waiting time to next eruption')
    ax2.set_title('Visualization of clustered data', y=1.02)
    ax2.set_aspect('equal')
    plt.tight_layout()
    #plt.suptitle(f'Silhouette analysis using k = k}',fontsize=16, fontweight='semibold', y=1.05)
    """
# Plot sse against k
#"""

"""
plt.figure(figsize=(6, 6))
plt.plot(list_k, sse, '-o')
plt.title('Elbow Method')
plt.xlabel(r'Number of clusters *k*')
plt.ylabel('Sum of Squared Distance');
"""


kmeans = KMeans(n_clusters=5)
kmeans.fit(X)
y_kmeans = kmeans.predict(X)

centers = kmeans.cluster_centers_
###ax.scatter3D(centers[:, 0], centers[:, 1], centers[:, 2], c='black', s=200, alpha=0.5);

img = ax.scatter3D(time_label, X[:, 3], X[:, 4], c=y_kmeans, cmap='viridis')
fig.colorbar(img)

plt.show()

gs = gridspec.GridSpec(9,1)
fig = plt.figure()
dot_size = 16

ax = fig.add_subplot(gs[0])
ax.scatter(time_label,x_accel,c=y_kmeans, cmap='viridis', s = dot_size)
ax.set_ylabel(r'X', size =16)

ax = fig.add_subplot(gs[1])
ax.scatter(time_label,y_accel,c=y_kmeans, cmap='viridis', s = dot_size )
ax.set_ylabel(r'Y', size =16)

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