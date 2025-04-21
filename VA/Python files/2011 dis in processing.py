#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 17:44:08 2024

@author: theorogers
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 15:41:55 2024

@author: theorogers
"""


#%% Cell 1, importing data and packages
import pandas as pd

l2021_dis_met_file_path = 'data sets/RAW/2 - 21LTLA dis in.xlsx'
l2011_dis_met_file_path = 'data sets/RAW/2 - 11CMLAD dis in.csv'

df_2021_dis_met = pd.read_excel(l2021_dis_met_file_path)
df_2011_dis_met = pd.read_csv(l2011_dis_met_file_path)

#%% Cell 2, finding disparencies between datasets

# Unique locations in 2011
unique_2011 = df_2011_dis_met[~df_2011_dis_met['geography'].isin(df_2021_dis_met['Lower tier local authorities'])]['geography'].unique()

# Unique locations in 2021
unique_2021 = df_2021_dis_met[~df_2021_dis_met['Lower tier local authorities'].isin(df_2011_dis_met['geography'])]['Lower tier local authorities'].unique()

print("Unique to 2011 dataset:")
print(unique_2011)

print("Unique to 2021 dataset:")
print(unique_2021)

#%% Cell 3, finding geographies in common


# Finding common values
common_values_2011 = df_2011_dis_met[df_2011_dis_met['geography'].isin(df_2021_dis_met['Lower tier local authorities'])]['geography']


# Count the number of common values 
common_count = len(common_values_2011.unique())

# Count the number of unique values 
uncommon_count = len(df_2011_dis_met[~df_2011_dis_met['geography'].isin(df_2021_dis_met['Lower tier local authorities'])]['geography'].unique()) + \
                 len(df_2021_dis_met[~df_2021_dis_met['Lower tier local authorities'].isin(df_2011_dis_met['geography'])]['Lower tier local authorities'].unique())

print("Number of common values between the datasets:", common_count)
print("Number of uncommon values between the datasets:", uncommon_count)

#%% Cell 4 , adjusting similar names

name_mapping = {
    'Kingston upon Hull, City of': 'Kingston upon Hull',
    'Herefordshire, County of': 'Herefordshire',
    'Bristol, City of': 'Bristol',
    'Cornwall,Isles of Scilly': 'Cornwall',
    'Shepway': 'Folkestone and Hythe',
    'The Vale of Glamorgan': 'Vale of Glamorgan'}

# Apply the map to the 2011 dataframe
df_2011_dis_met['Mapped geography'] = df_2011_dis_met['geography'].apply(lambda x: name_mapping.get(x, x))


#%% Cell 5 , amalgamating amalgamated locations

name_amalgamation = {
    'Corby': 'North Northamptonshire',
    'Daventry': 'West Northamptonshire',
    'East Northamptonshire': 'North Northamptonshire',
    'Kettering': 'North Northamptonshire',
    'Northampton': 'West Northamptonshire',
    'South Northamptonshire': 'West Northamptonshire',
    'Wellingborough': 'North Northamptonshire',

    'Forest Heath': 'West Suffolk',
    'St Edmundsbury': 'West Suffolk',
    'Suffolk Coastal': 'East Suffolk',
    'Waveney': 'East Suffolk',

    'Aylesbury Vale': 'Buckinghamshire',
    'Chiltern': 'Buckinghamshire',
    'South Bucks': 'Buckinghamshire',
    'Wycombe': 'Buckinghamshire',

    'Bournemouth': 'Bournemouth, Christchurch and Poole',
    'Christchurch': 'Bournemouth, Christchurch and Poole',
    'Poole': 'Bournemouth, Christchurch and Poole',

    'East Dorset': 'Dorset',
    'North Dorset': 'Dorset',
    'Purbeck': 'Dorset',
    'West Dorset': 'Dorset',
    'Weymouth and Portland': 'Dorset',

    'Taunton Deane': 'Somerset West and Taunton',
    'West Somerset': 'Somerset West and Taunton'
}


# Changing the name of the locations that are combined
df_2011_dis_met['Mapped geography'] = df_2011_dis_met['Mapped geography'].apply(lambda x: name_amalgamation.get(x, x))


# Define the columns to sum
sum_columns = [col for col in df_2011_dis_met.columns if col not in ['date', 'geography', 'geography code', 'Mapped geography']]

# Defining the rows with duplicate values, that require subsetting
rows_to_combine = df_2011_dis_met['Mapped geography'].duplicated(keep=False)

# Subsetting the rows
df_to_combine = df_2011_dis_met[rows_to_combine]
df_unchanged = df_2011_dis_met[~rows_to_combine]

# Group by the 'Mapped geography' column and sum the numeric columns
df_combined = df_to_combine.groupby('Mapped geography')[sum_columns].sum().reset_index()

# Concatenate the unchanged rows with the combined rows
df_2011_dis_met = pd.concat([df_unchanged, df_combined]).sort_values(by=['Mapped geography'])

# Reset index after concatenation
df_2011_dis_met.reset_index(drop=True, inplace=True)


#%% Cell 6, finding disparencies between new datasets

# Unique locations in 2011
unique_2011 = df_2011_dis_met[~df_2011_dis_met['Mapped geography'].isin(df_2021_dis_met['Lower tier local authorities'])]['Mapped geography'].unique()

# Unique locations in 2021
unique_2021 = df_2021_dis_met[~df_2021_dis_met['Lower tier local authorities'].isin(df_2011_dis_met['Mapped geography'])]['Lower tier local authorities'].unique()

print("Unique to 2011 dataset:")
print(unique_2011)

print("Unique to 2021 dataset:")
print(unique_2021)

#%% Cell 7, Fixing nan values

# Fill NaN values in the 'date' column with the date from the first entry
first_date = df_2011_dis_met['date'].iloc[0]
df_2011_dis_met['date'].fillna(first_date, inplace=True)

# Assign the values of 'Mapped geography' to the 'geography' column
df_2011_dis_met['geography'] = df_2011_dis_met['Mapped geography']

# Create a mapping dictionary from 'geography' to 'Lower tier local authorities Code'
geography_to_code_mapping = df_2021_dis_met.set_index('Lower tier local authorities')['Lower tier local authorities Code'].to_dict()

# Map 'geography' to 'Lower tier local authorities Code'
df_2011_dis_met['geography code'] = df_2011_dis_met['geography'].map(geography_to_code_mapping)

# Drop the 'Mapped geography' column
df_2011_dis_met.drop(columns=['Mapped geography'], inplace=True)

#%% Cell 8 saving to csv
df_2011_dis_met.to_excel("2 - 11CMLAD dis in pro.xlsx", index=False)




