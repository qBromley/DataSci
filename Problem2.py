# this is my kernel density function, it makes a 
def density_estimation(yMin,yMax,xMin,xMax,m1, m2, bandwidth=0.1):
    X, Y = np.mgrid[xMin:xMax:100j, yMin:yMax:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([m1, m2])
    kernel = stats.gaussian_kde(values, bw_method=bandwidth)
    Z = np.reshape(kernel(positions).T, X.shape)
    return X, Y, Z

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv('archive/movies_with_adjusted_gross.csv')
# Clean data by removing commas



# Drop rows with no data
df_cleaned = df.dropna(subset=['Gross Adjusted for Inflation (2023)', 'Metascore of movie'])
#calculating IQR by generating q1 and q3 using quantile function
Q1 = df_cleaned['Gross Adjusted for Inflation (2023)'].quantile(0.25)
Q3 = df_cleaned['Gross Adjusted for Inflation (2023)'].quantile(0.75)
#subtracting q1 and q3 to calculate IQR
IQR = Q3 - Q1
# bounding based on outlier range
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df_no_outliers = df_cleaned[(df_cleaned['Gross Adjusted for Inflation (2023)'] >= lower_bound) & (df_cleaned['Gross Adjusted for Inflation (2023)'] <= upper_bound)]


plt.figure(figsize=(15, 8))
sns.regplot(x='Metascore of movie', y='Gross Adjusted for Inflation (2023)', data=df_cleaned,line_kws={"color": "red"})
plt.xlabel('Metascore')
plt.ylabel('Gross Adjusted for Inflation (2023) Revenue')
plt.title('Scatter Plot of Gross Adjusted for Inflation (2023) Revenue by Metascore')
plt.savefig('adjusted/ScatterMetaGross.png')
plt.clf()

#Density of Movie rating and Gross Adjusted for Inflation (2023) income
xMin, xMax = 7,9
yMin, yMax = 0,1000
plt.figure(figsize=(10,8))
X, Y, Z = density_estimation(yMin, yMax,xMin,xMax,df_cleaned['Movie Rating'],df_cleaned['Gross Adjusted for Inflation (2023)'],.1)
cp = plt.contourf(X, Y, Z, levels=14, cmap='plasma')
plt.contour(X, Y, Z, levels=14, colors='white', linewidths=1.5)
plt.colorbar(cp, label='Density')
plt.title('Density Contour Map of Movie Ratings vs Gross Adjusted for Inflation (2023) Income')
plt.xlabel('Movie Rating')
plt.ylabel('Gross Adjusted for Inflation (2023) Income (Millions USD)')
plt.grid(True)
plt.savefig('adjusted/DensityRatingGross.png')
plt.clf()
#Density of Metascore and Gross Adjusted for Inflation (2023)
xMin, xMax = 60,100

plt.figure(figsize=(10,8))
X, Y, Z = density_estimation(yMin, yMax,xMin,xMax,df_cleaned['Metascore of movie'],df_cleaned['Gross Adjusted for Inflation (2023)'],.1)
cp = plt.contourf(X, Y, Z, levels=14, cmap='plasma')
plt.contour(X, Y, Z, levels=14, colors='white', linewidths=1.5)
plt.title('Density Contour Map of Critic ratings vs Gross Adjusted for Inflation (2023) Income')
plt.xlabel('Metascore of movie')
plt.ylabel('Gross Adjusted for Inflation (2023) Income (Millions USD)')
plt.grid(True)
plt.savefig('adjusted/DensityMetascoreGross.png')
plt.clf()



plt.figure(figsize=(15, 8))
sns.regplot(x='Movie Rating', y='Gross Adjusted for Inflation (2023)', data=df_cleaned,line_kws={"color": "red"})
plt.xlabel('Movie Rating')
plt.ylabel('Gross Adjusted for Inflation (2023) Revenue')
plt.title('Scatter Plot of Gross Adjusted for Inflation (2023) Revenue by Movie Rating')
plt.savefig('adjusted/ScatterAudianceGross.png')
plt.clf()



plt.figure(figsize=(15, 8))
sns.regplot(x='Metascore of movie', y='Gross Adjusted for Inflation (2023)', data=df_no_outliers,line_kws={"color": "red"})
plt.xlabel('Metascore')
plt.ylabel('Gross Adjusted for Inflation (2023) Revenue')
plt.title('Scatter Plot of Gross Adjusted for Inflation (2023) Revenue by Metascore')
plt.savefig('adjusted/ScatterOutliersRemovedMetaGross.png')
plt.clf()
#Correlegram
numeric_columns = ['Watch Time', 'Movie Rating', 'Metascore of movie', 'Gross Adjusted for Inflation (2023)', 'Votes']
corr_matrix_cleaned = df_cleaned[numeric_columns].corr()
plt.figure(figsize=(15, 8))
sns.heatmap(corr_matrix_cleaned, annot=True, cmap='seismic', linewidths=0.5,center = 0)
plt.savefig('adjusted/Corrlegram.png')
plt.clf()