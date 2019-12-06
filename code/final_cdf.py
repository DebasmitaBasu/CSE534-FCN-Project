import numpy as np
import matplotlib.pyplot as plt
import pandas
df = pandas.read_csv('stat - Ind.csv')
df1 = pandas.read_csv('stat - US.csv')
df = df.dropna()
df1 = df1.dropna()

prime = ['modern','high','goliath','mouse','Amazonprime']
netflix = ['13','1983','abstract','reality','Netflix']
youtube = ['nature','dubai','ub','Youtube']

prime_bw = []
netflix_bw = []
youtube_bw = []

prime_bw1 = []
netflix_bw1 = []
youtube_bw1 = []

for index, row in df.iterrows():
    for p in prime:
        if row['Name'].startswith(p):
            prime_bw.append(row['Throughput'])
            break
    for n in netflix:
        if row['Name'].startswith(n):
            netflix_bw.append(row['Throughput'])
            break
    for y in youtube:
        if row['Name'].startswith(y):
            youtube_bw.append(row['Throughput'])
            break

for index, row in df1.iterrows():
    for p in prime:
        if row['Name'].startswith(p):
            prime_bw1.append(row['Throughput'])
            break
    for n in netflix:
        if row['Name'].startswith(n):
            netflix_bw1.append(row['Throughput'])
            break
    for y in youtube:
        if row['Name'].startswith(y):
            youtube_bw1.append(row['Throughput'])
            break

x1 = np.array(prime_bw)
x2 = np.array(netflix_bw)
x3 = np.array(youtube_bw)
x4 = np.array(prime_bw1)
x5 = np.array(netflix_bw1)
x6 = np.array(youtube_bw1)
x1.sort()
x2.sort()
x3.sort()
x4.sort()
x5.sort()
x6.sort()
y1 = np.arange(1,len(x1)+1)/len(x1)
y2 = np.arange(1,len(x2)+1)/len(x2)
y3 = np.arange(1,len(x3)+1)/len(x3)
y4 = np.arange(1,len(x4)+1)/len(x4)
y5 = np.arange(1,len(x5)+1)/len(x5)
y6 = np.arange(1,len(x6)+1)/len(x6)
fig = plt.figure(figsize=(8,8))
ax=plt.subplot(111)
ax.plot(x1,y1,label='Prime - India')
ax.plot(x2,y2,label='Netflix - India')
ax.plot(x3,y3,label='YoutTube - India')
ax.plot(x4,y4,label='Prime - USA')
ax.plot(x5,y5,label='Netflix - USA')
ax.plot(x6,y6,label='YoutTube - USA')
ax.legend()
plt.title("CDF of Average Throughput using both WiFi and mobile networks")
plt.xlabel("Throughput in bps")
plt.ylabel("Fraction of Data")  
plt.show()
