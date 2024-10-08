import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv('archive/Top_1000_IMDb_movies_New_version.csv')
# Clean data by removing commas
df['Votes'] = df['Votes'].str.replace(',', '').astype(float)
df['Gross'] = pd.to_numeric(df['Gross'].str.replace(',', ''), errors='coerce')

# Drop rows with no data
df_cleaned = df.dropna(subset=['Gross', 'Metascore of movie'])
# just numeric colums
numeric_columns = ['Watch Time', 'Movie Rating', 'Metascore of movie', 'Gross', 'Votes']


#Correlegram
corr_matrix_cleaned = df_cleaned[numeric_columns].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix_cleaned, annot=True, cmap='seismic', linewidths=0.5, center = 0)
plt.savefig('Corrlegram.png')
plt.clf()
#box plot metascore and gross
#calculating iqr
Q1 = df_cleaned['Gross'].quantile(0.25)
Q3 = df_cleaned['Gross'].quantile(0.75)
IQR = Q3 - Q1
# bounding based on outlier range
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df_no_outliers = df_cleaned[(df_cleaned['Gross'] >= lower_bound) & (df_cleaned['Gross'] <= upper_bound)]

# figure with two subplots stacked vertically
fig, ax = plt.subplots(nrows=2, figsize=(15, 16))

# Scatter plot watch time and gross income
sns.regplot(x='Watch Time', y='Gross', data=df_cleaned, line_kws={"color": "red"}, ax=ax[0])
ax[0].set_xlabel('Watch Time', fontsize=16)
ax[0].set_ylabel('Gross Revenue', fontsize=16)
ax[0].set_title('Scatter Plot of Gross income by Watch Time', fontsize=16)

# Scatter plot watch time movie rating
sns.regplot(x='Watch Time', y='Movie Rating', data=df_cleaned, line_kws={"color": "red"}, ax=ax[1])
ax[1].set_xlabel('Watch Time', fontsize=16)
ax[1].set_ylabel('Movie Rating', fontsize=16)
ax[1].set_title('Scatter Plot of Movie Rating, by Watch Time', fontsize=16)

# prevent overlap
plt.tight_layout()
plt.savefig('StackedScatterWatchTime.png')
plt.clf()

#Scatterplot of metascore of movie and gross income with outliers removed usiing IQR
plt.figure(figsize=(15, 8))
sns.regplot(x='Metascore of movie', y='Gross', data=df_no_outliers,line_kws={"color": "red"})
plt.xlabel('Metascore')
plt.ylabel('Gross Revenue')
plt.title('Scatter Plot of Gross Revenue by Metascore')
plt.savefig('ScatterOutliersRemovedMetaGross.png')
plt.clf()





