import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv('archive/movies_with_adjusted_gross.csv')
# Clean data by removing commas




Q1 = df['Gross Adjusted for Inflation (2023)'].quantile(0.25)
Q3 = df['Gross Adjusted for Inflation (2023)'].quantile(0.75)
IQR = Q3 - Q1
# bounding based on outlier range
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df_no_outliers = df[(df['Gross Adjusted for Inflation (2023)'] >= lower_bound) & (df['Gross Adjusted for Inflation (2023)'] <= upper_bound)]



fig, ax = plt.subplots(nrows=2, figsize=(15, 16))

# Scatter plot watch time and gross income
sns.regplot(x='Watch Time', y='Gross', data=df, line_kws={"color": "red"}, ax=ax[0])
ax[0].set_xlabel('Watch Time', fontsize=16)
ax[0].set_ylabel('Gross Revenue', fontsize=16)
ax[0].set_title('Scatter Plot of Gross income by Watch Time', fontsize=16)

# Scatter plot watch time movie rating
sns.regplot(x='Watch Time', y='Movie Rating', data=df, line_kws={"color": "red"}, ax=ax[1])
ax[1].set_xlabel('Watch Time', fontsize=16)
ax[1].set_ylabel('Movie Rating', fontsize=16)
ax[1].set_title('Scatter Plot of Movie Rating, by Watch Time', fontsize=16)

# prevent overlap
plt.tight_layout()
plt.savefig('adjusted/StackedScatterWatchTime.png')
plt.clf()
plt.figure(figsize=(8, 15))

# creating bins for my boxplot
bins = [ 90, 135,170,230]
bin_labels = pd.cut(df['Watch Time'], bins=bins)
sns.violinplot(x=bin_labels, y='Gross Adjusted for Inflation (2023)', data=df)
plt.xlabel('Watch Time')
plt.ylabel('Gross Revenue')
plt.title('Box Plot of Gross Income by Watch Time Bins')
plt.savefig('adjusted/ViolinplotGrossIncome.png')
plt.clf()

bin_labels = pd.cut(df['Watch Time'], bins=bins)
sns.boxplot(x=bin_labels, y='Gross Adjusted for Inflation (2023)', data=df)
plt.xlabel('Watch Time')
plt.ylabel('Gross Revenue')
plt.title('Box Plot of Gross Income by Watch Time Bins')
plt.savefig('adjusted/BoxplotGrossIncome.png')
plt.clf()

# creating bins for my boxplot
bins = [ 90, 135,170,230]
bin_labels = pd.cut(df['Watch Time'], bins=bins)
sns.violinplot(x=bin_labels, y='Movie Rating', data=df)
plt.xlabel('Watch Time')
plt.ylabel('Audiance Score')
plt.title('Box Plot of Audiance Score by Watch Time Bins')
plt.savefig('adjusted/ViolinplotRating.png')
plt.clf()


bin_labels = pd.cut(df['Watch Time'], bins=bins)
sns.boxplot(x=bin_labels, y='Movie Rating', data=df)
plt.xlabel('Watch Time')
plt.ylabel('Audiance Score')
plt.title('Box Plot of Audiance Score by Watch Time Bins')
plt.savefig('adjusted/BoxplotRating.png')
plt.clf()
# Grabbing the means of the bins i made for audiance score and gross income 
avg_gross_per_bin = df.groupby(bin_labels,observed=True)['Gross Adjusted for Inflation (2023)'].mean()
avg_audiance_score_per_bin = df.groupby(bin_labels,observed=True)['Movie Rating'].mean()

#creating a bar plot for gross income vs watch time
plt.bar(x=avg_gross_per_bin.index.astype(str), height=avg_gross_per_bin)
plt.xlabel('Watch Time')
plt.ylabel('Average Gross Income (Adjusted)')
plt.title('Bar Plot of Average Gross Income')
plt.savefig('adjusted/BarplotGross')
plt.clf()
plt.bar(x=avg_audiance_score_per_bin.index.astype(str), height=avg_audiance_score_per_bin)
plt.xlabel('Watch Time')
plt.ylabel('Average Audiance Score')
plt.title('Bar Plot of Audiance Score')
plt.savefig('adjusted/BarplotAudiance')
plt.clf()