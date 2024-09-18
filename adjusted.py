import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats



movie_df = pd.read_csv('archive/Top_1000_IMDb_movies_New_version.csv')
movie_df['Votes'] = movie_df['Votes'].str.replace(',', '').astype(float)
movie_df['Gross'] = pd.to_numeric(movie_df['Gross'].str.replace(',', ''), errors='coerce')


df_cleaned = movie_df.dropna(subset=['Gross', 'Metascore of movie'])
inflation_df = pd.read_csv('archive/inflation.csv')

# ok this line is wack but its basically makeing a new col in the dataframe and creating the values by adding 1 to the inflation value of that year
# then it divides it by 100 and adds 1 to make it a number you can just multiply the gross income by, then i was having issues with the data being reversed so the .iloc[::-1] just reverse the data
#  so it is reversing the inflation rates, calculating the cumulitive product of all of them then reversing them back so they match the years.
inflation_df['Cumulative Inflation (to 2023)'] = (1 + inflation_df['Annual'] / 100).iloc[::-1].cumprod().iloc[::-1]

conversion_df = inflation_df[['Year', 'Cumulative Inflation (to 2023)']].copy()

# Removing rows with missing years and dropping rows with empty years and making sure all data types are Ints
df_cleaned['Year of Release'] = df_cleaned['Year of Release'].str.extract('(\d{4})')
df_cleaned = df_cleaned.dropna(subset=['Year of Release']) 
df_cleaned['Year of Release'] = df_cleaned['Year of Release'].astype(int)

#Remove any rows with Year of Release before 1954
df_cleaned = df_cleaned[df_cleaned['Year of Release'] >= 1954]

merged_df = pd.merge(df_cleaned, conversion_df, left_on='Year of Release', right_on='Year', how='left')

merged_df['Gross Adjusted for Inflation (2023)'] = merged_df['Gross'] * merged_df['Cumulative Inflation (to 2023)']



merged_df.to_csv('archive/movies_with_adjusted_gross.csv', index=False)




