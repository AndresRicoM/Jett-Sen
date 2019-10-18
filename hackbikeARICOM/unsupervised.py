#%matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
import numpy as np
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
from mpl_toolkits.mplot3d import Axes3D

#X, y_true = make_blobs(n_samples=300, centers=4,
#                       cluster_std=0.60, random_state=0)
current_data = np.genfromtxt('/home/aricom/Desktop/HackBike/2019-10-17 16:36:17.625353.txt', delimiter = ',',  dtype='str')
torque = current_data[:,[8]]
torque = torque.astype(np.float)
x_accel = current_data[:,[20]]
x_accel = x_accel.astype(np.float)
y_accel = current_data[:,[21]]
y_accel = y_accel.astype(np.float)
z_accel = current_data[:,[22]]
z_accel = z_accel.astype(np.float)
speed = current_data[:,[18]]
speed = speed.astype(np.float)

X = np.hstack((x_accel,y_accel))
X = np.hstack((X,z_accel))
X = np.hstack((X,torque))
X = np.hstack((X,speed))

plt.style.use('dark_background')

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(X[:, 0], X[:, 1],X[:, 2] , s=50);

#"""
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

# Plot sse against k
#"""

"""
plt.figure(figsize=(6, 6))
plt.plot(list_k, sse, '-o')
plt.title('Elbow Method')
plt.xlabel(r'Number of clusters *k*')
plt.ylabel('Sum of Squared Distance');
"""


"""kmeans = KMeans(n_clusters=6)
kmeans.fit(X)
y_kmeans = kmeans.predict(X)

centers = kmeans.cluster_centers_
###ax.scatter3D(centers[:, 0], centers[:, 1], centers[:, 2], c='black', s=200, alpha=0.5);

img = ax.scatter3D(X[:, 3], X[:, 4], X[:, 0], c=y_kmeans, cmap='viridis')
fig.colorbar(img)"""

plt.show()
