import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import pearsonr
df = pd.read_csv('archive/movies_with_adjusted_gross.csv')
# Clean data by removing commas




Q1 = df['Gross Adjusted for Inflation (2023)'].quantile(0.25)
Q3 = df['Gross Adjusted for Inflation (2023)'].quantile(0.75)
IQR = Q3 - Q1
# bounding based on outlier range
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df_no_outliers = df[(df['Gross Adjusted for Inflation (2023)'] >= lower_bound) & (df['Gross Adjusted for Inflation (2023)'] <= upper_bound)]


# creating bins for my plots
bins = [90, 135, 170, 230]
bin_names = ['90-135', '135-170', '170+']  
bin_labels = pd.cut(df['Watch Time'], bins=bins, labels=bin_names)

fig, ax = plt.subplots(ncols=2, figsize=(16, 9))
sns.violinplot(x=bin_labels, y='Gross Adjusted for Inflation (2023)', data=df,hue=bin_labels,legend='auto',ax=ax[1])
ax[1].set_xlabel('Watch Time',fontsize=16)
ax[1].set_ylabel('Gross Revenue',fontsize=16)
ax[1].set_title('Violin Plot of Gross Income by Watch Time Bins',fontsize=16)


sns.violinplot(x=bin_labels, y='Movie Rating', data=df,hue=bin_labels,ax=ax[0])
ax[0].set_xlabel('Watch Time',fontsize=16)
ax[0].set_ylabel('Audiance Score',fontsize=16)
ax[0].set_title('Violin plot of Audiance Score by Watch Time Bins',fontsize=16)

plt.tight_layout()
plt.savefig('adjusted/DualViolinPlot')
plt.clf()

# Grabbing the means of the bins i made for audiance score and gross income 
avg_gross_per_bin = df.groupby(bin_labels,observed=True)['Gross Adjusted for Inflation (2023)'].mean()
avg_audiance_score_per_bin = df.groupby(bin_labels,observed=True)['Movie Rating'].mean()

#creating a bar plot for gross income vs watch time

palette = ['blue', 'orange', 'green']

fig, ax = plt.subplots(ncols=2, figsize=(16, 9))

# Bar plot for average gross income with matching colors
ax[0].bar(x=avg_gross_per_bin.index.astype(str), height=avg_gross_per_bin, color=palette)
ax[0].set_xlabel('Watch Time')
ax[0].set_ylabel('Average Gross Income (Adjusted)')
ax[0].set_title('Bar Plot of Average Gross Income')

# Bar plot for average audience score with matching colors
ax[1].bar(x=avg_audiance_score_per_bin.index.astype(str), height=avg_audiance_score_per_bin, color=palette)
ax[1].set_xlabel('Watch Time')
ax[1].set_ylabel('Average Audience Score')
ax[1].set_title('Bar Plot of Audience Score')

# Save the figure
plt.tight_layout()
plt.savefig('adjusted/DualBarplot.png')
plt.clf()

#hypothesis testing for watch time and gross income
X = df['Watch Time']  # independent variable
y = df['Gross Adjusted for Inflation (2023)']  # dependent variable

stat, p = pearsonr(X, y)
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
 print('There is no linear correlation between the runtime of a movie and its Gross Income')
else:
 print('There is a linear correlation between the runtime of a movie and its Gross Income')
 #hypothesis testing for watch time and movie rating \ audiance score
X = df['Watch Time']  # independent variable
y = df['Movie Rating']  # dependent variable

stat, p = pearsonr(X, y)
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
 print('There is no linear correlation between the runtime of a movie and its Audiance Score')
else:
 print('There is a linear correlation between the runtime of a movie and its Audiance Score')