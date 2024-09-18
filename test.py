import pandas as pd

# Specify the path to your Excel file
file_path = 'archive/SeriesReport-20240917212009_e990b0.xlsx'

# Read the entire Excel file (default loads all rows and columns)
df = pd.read_excel(file_path)

# Display the DataFrame to check all lines
print(df)
