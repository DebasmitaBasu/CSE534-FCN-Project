import matplotlib.pyplot as plt
#from google.colab import files
# Data to plot
labels = 'TCP', 'UDP'
sizes = [12, 20]
colors = ['lightcoral', 'lightskyblue']
#explode = (0.1, 0, 0, 0)  # explode 1st slice

# Plot
plt.pie(sizes, #explode=explode, 
        labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')
plt.title("Percentage of YouTube sessions using two different transport layer protocols")
plt.show()
#plt.savefig("pie.png")
#files.download("pie.png") 
