#from google.colab import files

import numpy as np
import matplotlib.pyplot as plt
import pandas
df = pandas.read_csv('stat - USwifi.csv')
df = df.dropna()

prime = ['modern','high','goliath','mouse','Amazonprime']
netflix = ['13','1983','abstract','reality','Netflix']
youtube = ['nature','dubai','ub','Youtube']

prime_bw = []
netflix_bw = []
youtube_bw = []

for index, row in df.iterrows():
    for p in prime:
        if row['Name'].startswith(p):
            prime_bw.append(row['Flows'])
            break
    for n in netflix:
        if row['Name'].startswith(n):
            netflix_bw.append(row['Flows'])
            break
    for y in youtube:
        if row['Name'].startswith(y):
            youtube_bw.append(row['Flows'])
            break

x1 = np.array(prime_bw)
x2 = np.array(netflix_bw)
x3 = np.array(youtube_bw)

kwargs = dict(alpha=0.5, bins=5)

plt.hist(x1, **kwargs, color='g', label='Amazon Prime')
plt.hist(x2, **kwargs, color='b', label='Netflix')
plt.hist(x3, **kwargs, color='r', label='YouTube')
plt.gca().set(title='Number of streams in a single session of different apps', ylabel='Frequency', xlabel='No. of streams')
#plt.xlim(50,75)
plt.legend();
plt.show()
#plt.savefig("abc.png")
#files.download("abc.png") 
