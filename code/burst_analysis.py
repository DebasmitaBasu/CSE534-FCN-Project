import pandas as pd
import seaborn as sns
from google.colab import files
import io

uploaded = files.upload()

df1 = pd.read_csv(io.BytesIO(uploaded['BurstsNo.csv']))

sns_plt = sns.boxplot(x='Interval',y='NumBursts',hue='App', data=df1)

sns_plt.figure.savefig("boxplot.png")
files.download("boxplot.png") 
