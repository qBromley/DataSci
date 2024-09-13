import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv('/home/quinn/DataSci/archive/Top_1000_IMDb_movies_New_version.csv')
# Clean data by removing commas
df['Votes'] = df['Votes'].str.replace(',', '').astype(float)
df['Gross'] = pd.to_numeric(df['Gross'].str.replace(',', ''), errors='coerce')

# Drop rows with no data
df_cleaned = df.dropna(subset=['Gross'])
# just numeric colums
numeric_columns = ['Watch Time', 'Movie Rating', 'Metascore of movie', 'Gross', 'Votes']


#Correlegram
corr_matrix_cleaned = df_cleaned[numeric_columns].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix_cleaned, annot=True, cmap='seismic', linewidths=0.5, center = 0)
plt.savefig('/home/quinn/DataSci/correlogram.png')
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

plt.figure(figsize=(15, 8))
sns.regplot(x='Metascore of movie', y='Gross', data=df_cleaned,line_kws={"color": "red"})
plt.xlabel('Metascore')
plt.ylabel('Gross Revenue')
plt.title('Scatter Plot of Gross Revenue by Metascore')
plt.savefig('/home/quinn/DataSci/ScatterMetaGross.png')
plt.clf()

plt.figure(figsize=(15, 8))
sns.regplot(x='Metascore of movie', y='Gross', data=df_no_outliers,line_kws={"color": "red"})
plt.xlabel('Metascore')
plt.ylabel('Gross Revenue')
plt.title('Scatter Plot of Gross Revenue by Metascore')
plt.savefig('/home/quinn/DataSci/ScatterOutliersRemovedMetaGross.png')
plt.clf()

#box plot showing 
bins = [0, 60, 80, 100]
labels = ['Low(0-60)', 'Medium(60-80)', 'High(80-100)']
df_cleaned = df_no_outliers.copy()
df_cleaned.loc[:, 'Metascore_binned'] = pd.cut(df_cleaned['Metascore of movie'], bins=bins, labels=labels, right=False)

# Create the box plot using the binned Metascore
plt.figure(figsize=(10, 20))
sns.boxplot(x='Metascore_binned', y='Gross', data=df_cleaned)
plt.xlabel('Metascore Category')
plt.ylabel('Gross Revenue')
plt.title('Box Plot of Gross Revenue by Binned Metascore')
plt.savefig('/home/quinn/DataSci/BoxPlotMetaGross.png')




