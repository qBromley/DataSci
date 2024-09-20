import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv('archive/movies_with_adjusted_gross.csv')
# Clean data by removing commas



# Drop rows with no data
df_cleaned = df.dropna(subset=['Gross Adjusted for Inflation (2023)', 'Metascore of movie'])
Q1 = df_cleaned['Gross Adjusted for Inflation (2023)'].quantile(0.25)
Q3 = df_cleaned['Gross Adjusted for Inflation (2023)'].quantile(0.75)
IQR = Q3 - Q1
# bounding based on outlier range
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df_no_outliers = df_cleaned[(df_cleaned['Gross Adjusted for Inflation (2023)'] >= lower_bound) & (df_cleaned['Gross Adjusted for Inflation (2023)'] <= upper_bound)]



plt.figure(figsize=(15, 8))
sns.regplot(x='Movie Rating', y='Gross Adjusted for Inflation (2023)', data=df_cleaned,line_kws={"color": "red"})
plt.xlabel('Movie Rating')
plt.ylabel('Gross Adjusted for Inflation (2023) Revenue')
plt.title('Scatter Plot of Gross Adjusted for Inflation (2023) Revenue by Movie Rating')
plt.savefig('adjusted/ScatterAudianceGross.png')
plt.clf()
plt.savefig('adjusted/Bubbleplot.png')