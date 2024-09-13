import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv('/home/quinn/DataSci/archive/Top_1000_IMDb_movies_New_version.csv',usecols=[ 3, 4, 5, 6, 7])
df['Votes'] = df['Votes'].str.replace(',', '').astype(float)
df['Gross'] = pd.to_numeric(df['Gross'].str.replace(',', ''), errors='coerce')
df_cleaned = df.dropna(subset=['Gross'])
numeric_columns = ['Watch Time', 'Movie Rating', 'Metascore of movie', 'Gross', 'Votes']
corr_matrix_cleaned = df_cleaned[numeric_columns].corr()
plt.figure(figsize=(10, 8))

# Create the heatmap for the cleaned data
sns.heatmap(corr_matrix_cleaned, annot=True, cmap='coolwarm', linewidths=0.5)

# Show the plot
plt.show()
# data['Year of Release'] = data['Year of Release'].str.replace('I', '', regex=False)
# print(int(data['Year of Release']))

# corrlation = data.corr()
# plt.figure(figsize=(10, 8))
# sns.heatmap(corrlation, annot=True, cmap='coolwarm', linewidths=0.5)
# plt.show()
