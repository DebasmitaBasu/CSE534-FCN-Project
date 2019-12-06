from google.colab import files
import matplotlib.pyplot as plt
import numpy as np

x1=[5,6,5,5,4,6,5]
x2=[5,4,5,4,5,5,6]
x3=[5,6,6,5,4,5,4]

n_bins = 10
x = [[5,4,5,4,5,5,6],[5,6,6,5,4,5,4],[5,6,5,5,4,6,5]]
labels = ["Amazon Prime","Netflix", "YouTube"]
colors = ['green', 'tan', 'skyblue']
plt.hist(x, n_bins, density=True, histtype='bar', color=colors, label=labels)
plt.legend(prop={'size': 10})
plt.gca().set(title='RTT of different apps', ylabel='Frequency', xlabel='RTT')

#plt.show()
plt.savefig("rtt_hist.png")
files.download("rtt_hist.png")