# Part 1: Data Cleaning and Exploration (Python)

import pandas as pd

# 1. Loading the dataset and checking the first 5 rows.
data = pd.read_csv('/mnt/data/crime_data.csv')
print(data.head())

# 2. Identifing columns with missing values and their respective counts and dropping columns where more than 50% of the data is missing.
missing_counts = data.isnull().sum()
print(missing_counts[missing_counts > 0])

# Dropping columns with more than 50% missing data
threshold = len(data) * 0.5
data_cleaned = data.loc[:, missing_counts < threshold]

# 3. Converting DATE OCC column to datetime format. Extracting year, month, day. Creating new column for the hour using TIME OCC.
data_cleaned['DATE OCC'] = pd.to_datetime(data_cleaned['DATE OCC'], errors='coerce')
data_cleaned['Year'] = data_cleaned['DATE OCC'].dt.year
data_cleaned['Month'] = data_cleaned['DATE OCC'].dt.month
data_cleaned['Day'] = data_cleaned['DATE OCC'].dt.day

# Assuming TIME OCC is in HHMM format
data_cleaned['Hour'] = data_cleaned['TIME OCC'].astype(str).str.zfill(4).str[:2].astype(int)

# 4. Filtering dataset for crimes in 2023 and BURGLARY in Crm Cd Desc.
crimes_2023 = data_cleaned[data_cleaned['Year'] == 2023]
burglary_2023 = crimes_2023[crimes_2023['Crm Cd Desc'].str.contains('BURGLARY', case=False, na=False)]

# 5. Grouping by AREA NAME, calculate total number of crimes and average victim age and sorting by total crimes.
grouped_area = data_cleaned.groupby('AREA NAME').agg(
    Total_Crimes=('Crm Cd', 'count'),
    Avg_Victim_Age=('Vict Age', 'mean')
).sort_values(by='Total_Crimes', ascending=False)

print(grouped_area)

# Part 2: Further Exploration 

# 1. Top 3 most frequent Crm Cd Desc values
top_crimes = data_cleaned['Crm Cd Desc'].value_counts().head(3)
print(top_crimes)

# 2. Grouping by Hour and count number of crimes
crimes_by_hour = data_cleaned.groupby('Hour').size()
print(crimes_by_hour)

# 3. Grouping by Vict Sex, calculate total crimes, average victim age
vict_sex_stats = data_cleaned.groupby('Vict Sex').agg(
    Total_Crimes=('Crm Cd', 'count'),
    Avg_Victim_Age=('Vict Age', 'mean')
)
print(vict_sex_stats)

# Part 4: Advanced Analysis 

# Create Severity Score
data_cleaned['Severity Score'] = (
    (data_cleaned['Weapon Used Cd'].notnull().astype(int) * 5) +
    (data_cleaned['Crm Cd Desc'].str.contains('BURGLARY', case=False, na=False).astype(int) * 3) +
    (~data_cleaned['Crm Cd Desc'].str.contains('BURGLARY', case=False, na=False).astype(int))
)

# Group by AREA NAME and find total severity score
severity_by_area = data_cleaned.groupby('AREA NAME')['Severity Score'].sum()
print(severity_by_area)

