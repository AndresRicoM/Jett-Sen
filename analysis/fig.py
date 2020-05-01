import sys
import os
import pickle
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

url = '/Users/AndresRico/Desktop/working/Jett-Sen/analysis/sse/'

fx = url + 'hackbike-jupyter-006f16e0-3235-11ea-9980-e166d58b4532.txt'
ff = url + 'fullhackbike-jupyter-006f16e0-3235-11ea-9980-e166d58b4532.txt'
fm = url + 'combined_jupyter.txt'

list_k = list(range(1, 50))

with open(fx, "rb") as fp:
        x = pickle.load(fp)

with open(ff, "rb") as fp:
        f = pickle.load(fp)

with open(fm, "rb") as fp:
        m = pickle.load(fp)

normx = [(float(i)-min(x))/(max(x)-min(x)) for i in x]
normf = [(float(i)-min(f))/(max(f)-min(f)) for i in f]
normm = [(float(i)-min(m))/(max(m)-min(m)) for i in m]

plt.figure(figsize=(6, 6))
plt.plot(list_k, normx, '-o', color = 'red', label = 'x')
plt.plot(list_k, normf, '-o', color = 'blue', label = 'fusion')
plt.plot(list_k, normm, '-o', color = 'green', label = 'multiple')
plt.title('Elbow Curve Analysis', fontsize=30)
plt.xlabel(r'Number of clusters *k*', fontsize=25)
plt.ylabel('Sum of Squared Distance', fontsize=25);
plt.legend()

plt.show()
