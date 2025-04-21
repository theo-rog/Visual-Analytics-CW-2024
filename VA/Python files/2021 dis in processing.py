#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 20:49:33 2024

@author: theorogers
"""


#%% Cell 1, importing data and packages
import pandas as pd
import os


#Directory work
script_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(script_dir)


pro_2011_dis_in_file_path = 'data sets/Processed/2 - 11CMLAD dis in pro PIVOT.xlsx'

l2021_dis_in_file_path = 'data sets/RAW/2 - 21LTLA dis in.xlsx'


df_2021_dis_in = pd.read_excel(l2021_dis_in_file_path)
df_2011_dis_in = pd.read_excel(pro_2011_dis_in_file_path)

df_2021_dis_in = df_2021_dis_in.rename(columns={
    "Lower tier local authorities": "geography",
    "Lower tier local authorities Code": "geography code"
})

df_2021_dis_in['date'] = 2021

#%% Cell 2, finding geographical disparencies between datasets

# Unique locations in 2011
unique_2011 = df_2011_dis_in[~df_2011_dis_in['geography'].isin(df_2021_dis_in['geography'])]['geography'].unique()

# Unique locations in 2021
unique_2021 = df_2021_dis_in[~df_2021_dis_in['geography'].isin(df_2011_dis_in['geography'])]['geography'].unique()

print("Unique to 2011 dataset:")
print(unique_2011)

print("Unique to 2021 dataset:")
print(unique_2021)

df_2021_dis_in.rename(columns={'Industry (current) (19 categories)': 'Industry'}, inplace=True)
df_2021_dis_in.drop(columns=['Industry (current) (19 categories) Code'], inplace=True)

df_2021_dis_in.rename(columns={'Distance travelled to work (10 categories)': 'Distance travelled to work'}, inplace=True)
df_2021_dis_in.drop(columns=['Distance travelled to work (10 categories) Code'], inplace=True)

df_2021_dis_in.rename(columns={'Observation': 'Count'}, inplace=True)

#%% Cell 3.3 Combining COL and Westminster

# Combine 'City of London' and 'Westminster' into one category.
df_2021_dis_in['geography'] = df_2021_dis_in['geography'].replace(['City of London', 'Westminster'], 'Westminster,City of London')

#Combine 'Cornwall' and 'Isles of Scilly' into one category.
df_2011_dis_in['geography'] = df_2011_dis_in['geography'].replace(['Cornwall', 'Isles of Scilly'], 'Cornwall, Isles of Scilly')
df_2021_dis_in['geography'] = df_2021_dis_in['geography'].replace(['Cornwall', 'Isles of Scilly'], 'Cornwall, Isles of Scilly')

# Group by the new 'geography', 'Industry', and 'Distance travelled to work', then sum the 'Value'.
df_2021_dis_in = df_2021_dis_in.groupby(['geography code','date', 'geography', 'Industry', 'Distance travelled to work'])['Count'].sum().reset_index()


# Unique locations in 2011
unique_2011 = df_2011_dis_in[~df_2011_dis_in['geography'].isin(df_2021_dis_in['geography'])]['geography'].unique()

# Unique locations in 2021
unique_2021 = df_2021_dis_in[~df_2021_dis_in['geography'].isin(df_2011_dis_in['geography'])]['geography'].unique()

print("Unique to 2011 dataset:")
print(unique_2011)

print("Unique to 2021 dataset:")
print(unique_2021)


#%% Cell 4, finding Industry disparencies between datasets

# Unique Industry in 2011
unique_2011 = df_2011_dis_in[~df_2011_dis_in['Industry'].isin(df_2021_dis_in['Industry'])]['Industry'].unique()

# Unique Industry in 2021
unique_2021 = df_2021_dis_in[~df_2021_dis_in['Industry'].isin(df_2011_dis_in['Industry'])]['Industry'].unique()

print("Unique to 2011 dataset:")
print(unique_2011)

print("Unique to 2021 dataset:")
print(unique_2021)


# Replace colon with semicolon in 'Industry' column of df_2021_dis_in
df_2011_dis_in['Industry'] = df_2011_dis_in['Industry'].str.replace(r':\s', '; ', regex=True)

# Remove the 'Not in employment or aged 15 years and under' category in the 2021 dataset
df_2021_dis_in = df_2021_dis_in[df_2021_dis_in['Industry'] != 'Does not apply']


# Unique Industry in 2011
unique_2011 = df_2011_dis_in[~df_2011_dis_in['Industry'].isin(df_2021_dis_in['Industry'])]['Industry'].unique()

# Unique Industry in 2021
unique_2021 = df_2021_dis_in[~df_2021_dis_in['Industry'].isin(df_2011_dis_in['Industry'])]['Industry'].unique()

print("Unique to 2011 dataset:")
print(unique_2011)

print("Unique to 2021 dataset:")
print(unique_2021)


#%% Cell 5, finding disparencies between datasets

# Remove leading spaces from values in the 'Industry' column in df_2011_dis_in

df_2021_dis_in['Distance travelled to work'] = df_2021_dis_in['Distance travelled to work'].replace('Not in employment or works mainly offshore, in no fixed place or outside the UK', 'Other')
df_2011_dis_in['Distance travelled to work'] = df_2011_dis_in['Distance travelled to work'].replace('Work mainly at or from home', 'Works mainly from home')
  

# Ensure the dataframe is sorted by geography and distance travelled to work (if necessary)
df_2021_dis_in = df_2021_dis_in.sort_values(by=['geography', 'Industry'])

# Unique Industry in 2011
unique_2011 = df_2011_dis_in[~df_2011_dis_in['Distance travelled to work'].isin(df_2021_dis_in['Distance travelled to work'])]['Distance travelled to work'].unique()

# Unique Industry in 2021
unique_2021 = df_2021_dis_in[~df_2021_dis_in['Distance travelled to work'].isin(df_2011_dis_in['Distance travelled to work'])]['Distance travelled to work'].unique()

print("Unique to 2011 dataset:")
print(unique_2011)

print("Unique to 2021 dataset:")
print(unique_2021)


#%% Cell 7 removing duplicate entries


print("Rows in 2011 after processing:", len(df_2011_dis_in))
print("Rows in 2021 after processing:", len(df_2021_dis_in))

# Check for duplicates
print("Duplicates in 2011:", df_2011_dis_in.duplicated().sum())
print("Duplicates in 2021:", df_2021_dis_in.duplicated().sum())

# Duplicate rows
duplicate_rows = df_2021_dis_in[df_2021_dis_in.duplicated(['geography', 'Industry', 'Distance travelled to work'], keep='first')]


all_categories_2021 = df_2021_dis_in[df_2021_dis_in['Industry'] == 'All categories']
print("Additional 'All categories' rows in 2021:", all_categories_2021.shape[0])

# Check if concatenation created duplicate entries
print("Check for unexpected duplicate rows after concatenation in 2021:", df_2021_dis_in[df_2021_dis_in.duplicated(['geography', 'Industry', 'Distance travelled to work'], keep=False)].shape[0])

# Remove duplicates in 2021 dataset
df_2021_dis_in = df_2021_dis_in.drop_duplicates()

# Check how many rows are there after removing duplicates
print("Rows in 2021 after removing duplicates:", df_2021_dis_in.shape[0])

# Verify that 'All categories' rows are not duplicates
df_2021_dis_in = df_2021_dis_in.drop_duplicates(subset=['geography', 'Industry', 'Distance travelled to work'])

# Recheck unexpected duplicates after potential resolution
print("Recheck for unexpected duplicate rows after attempting resolution in 2021:", df_2021_dis_in[df_2021_dis_in.duplicated(['geography', 'Industry', 'Distance travelled to work'], keep=False)].shape[0])

#%% Cell 8 combining 
df_2021_dis_in['date'] = 2021

#Removing 'All categories'
df_2021_dis_in = df_2021_dis_in[df_2021_dis_in['Industry'] != 'All categories']
df_2021_dis_in = df_2021_dis_in[df_2021_dis_in['Distance travelled to work'] != 'All categories']
df_2011_dis_in = df_2011_dis_in[df_2011_dis_in['Industry'] != 'All categories']
df_2011_dis_in = df_2011_dis_in[df_2011_dis_in['Distance travelled to work'] != 'All categories']

#Replacing strings so ordinal data is in order when alphabetised
df_2011_dis_in['Distance travelled to work'] = df_2011_dis_in['Distance travelled to work'].str.replace('less than 2km', '2km or less')
df_2021_dis_in['Distance travelled to work'] = df_2021_dis_in['Distance travelled to work'].str.replace('less than 2km', '2km or less')


# Merging the 2011 and 2021 datasets on the keys
merged_df = pd.merge(df_2011_dis_in, df_2021_dis_in, on=['geography', 'Distance travelled to work', 'Industry', 'geography code'], suffixes=('_2011', '_2021'))

# Calculating the difference in 'Count' between 2021 and 2011
merged_df['Count'] = merged_df['Count_2021'] - merged_df['Count_2011']
merged_df['date'] = "change"

# Creating the new dataframe to include only the required columns
df_1121_dis_in = merged_df[['geography', 'Distance travelled to work', 'date', 'Industry', 'geography code', 'Count']]


df_1121_dis_in = pd.concat([df_2011_dis_in, df_2021_dis_in, df_1121_dis_in], ignore_index=True)



# Saving the new dataframe or you can directly use it
df_1121_dis_in.to_excel('df_1121_dis_in_change.xlsx', index=False)



                                                                                   