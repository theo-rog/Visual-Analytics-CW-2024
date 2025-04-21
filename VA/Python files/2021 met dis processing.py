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

pro_2011_dis_met_file_path = 'data sets/Processed/2 - 11CMLAD met dis pro PIVOT.xlsx'

l2021_dis_met_file_path = 'data sets/RAW/2 - 21LTLA met dis.csv'


df_2021_dis_met = pd.read_csv(l2021_dis_met_file_path)
df_2011_dis_met = pd.read_excel(pro_2011_dis_met_file_path)
 

#%% Cell 2, finding geographical disparencies between datasets

# Unique locations in 2011
unique_2011 = df_2011_dis_met[~df_2011_dis_met['geography'].isin(df_2021_dis_met['geography'])]['geography'].unique()

# Unique locations in 2021
unique_2021 = df_2021_dis_met[~df_2021_dis_met['geography'].isin(df_2011_dis_met['geography'])]['geography'].unique()

print("Unique to 2011 dataset:")
print(unique_2011)

print("Unique to 2021 dataset:")
print(unique_2021)


#%% Cell 3.3 Combining COL and Westminster

# Combine 'City of London' and 'Westminster' into one category.
df_2021_dis_met['geography'] = df_2021_dis_met['geography'].replace(['City of London', 'Westminster'], 'Westminster,City of London')

# Group by the new 'geography', 'Method of travel to work', and 'Distance travelled to work', then sum the 'Value'.
df_2021_dis_met = df_2021_dis_met.groupby(['geography', 'Method of travel to work', 'Distance travelled to work'])['Count'].sum().reset_index()

# Unique locations in 2011
unique_2011 = df_2011_dis_met[~df_2011_dis_met['geography'].isin(df_2021_dis_met['geography'])]['geography'].unique()

# Unique locations in 2021
unique_2021 = df_2021_dis_met[~df_2021_dis_met['geography'].isin(df_2011_dis_met['geography'])]['geography'].unique()

print("Unique to 2011 dataset:")
print(unique_2011)

print("Unique to 2021 dataset:")
print(unique_2021)


#%% Cell 4, finding disparencies between datasets

# Remove leading spaces from values in the 'Method of travel to work' column in df_2011_dis_met
df_2011_dis_met['Method of travel to work'] = df_2011_dis_met['Method of travel to work'].str.strip()

def merge_travel_methods(df,method1,method2,comb_name):
    # Replace values to be merged into one category
    df['Method of travel to work'] = df['Method of travel to work'].replace([method1, method2], comb_name)

    # Group by the new 'Method of travel to work', 'Other columns you want to group by', then sum the 'Count' column.
    df = df.groupby(['Method of travel to work', 'geography', 'Distance travelled to work'])['Count'].sum().reset_index()

    return df

merge_travel_methods(df_2021_dis_met,'Train','Underground, metro, light rail, tram','Train, underground, metro, light rail or tram')
merge_travel_methods(df_2021_dis_met,'Other method of travel to work','Motorcycle, scooter or moped','All other methods of travel to work')
merge_travel_methods(df_2021_dis_met,'All other methods of travel to work','Taxi','All other methods of travel to work')

# Remove the 'Not in employment or aged 15 years and under' category in the 2021 dataset
df_2021_dis_met = df_2021_dis_met[df_2021_dis_met['Method of travel to work'] != 'Not in employment or aged 15 years and under']


## Creating all categories
# Sum 'Count' for each unique 'Geography' and 'Distance travelled to work' combination in the 2021 dataset
all_categories_2021 = df_2021_dis_met.groupby(['geography', 'Distance travelled to work'])['Count'].sum().reset_index()

# Add a new column for 'Method of travel to work' with the value 'All categories'
all_categories_2021['Method of travel to work'] = 'All categories'

# Append this new dataframe to the existing 2021 dataframe
df_2021_dis_met = pd.concat([df_2021_dis_met, all_categories_2021])

# Ensure the dataframe is sorted by geography and distance travelled to work (if necessary)
df_2021_dis_met = df_2021_dis_met.sort_values(by=['geography', 'Distance travelled to work'])



# Unique methods of travel to work in 2011
unique_2011 = df_2011_dis_met[~df_2011_dis_met['Method of travel to work'].isin(df_2021_dis_met['Method of travel to work'])]['Method of travel to work'].unique()

# Unique methods of travel to work in 2021
unique_2021 = df_2021_dis_met[~df_2021_dis_met['Method of travel to work'].isin(df_2011_dis_met['Method of travel to work'])]['Method of travel to work'].unique()

print("Unique to 2011 dataset:")
print(unique_2011)

print("Unique to 2021 dataset:")
print(unique_2021)

#%% Cell 5, checking
def check_all_categories(df, col):
    if col == 'Method of travel to work':
        colnt = 'Distance travelled to work'
    elif col == 'Distance travelled to work':
        colnt = 'Method of travel to work'
    else:
        print("Err")
    # Group by 'Geography' and 'Distance travelled to work' and verify the sum equals the 'All categories' entry
    grouped = df.groupby(['geography', colnt])
    
    for name, group in grouped:
        all_cat_count = group[group[col] == 'All categories']['Count'].sum()
        sum_of_others = group[group[col] != 'All categories']['Count'].sum()
        
        if all_cat_count != sum_of_others:
            print(f"Discrepancy found for {name}: All categories count is {all_cat_count}, sum of {col} is {sum_of_others}")
            return False
    print("All 'All categories' counts are correct.")
    return True

check_all_categories(df_2011_dis_met,'Method of travel to work')
check_all_categories(df_2021_dis_met,'Method of travel to work')

#%% Cell 6, finding disparencies between datasets

# Remove leading spaces from values in the 'Method of travel to work' column in df_2011_dis_met
df_2011_dis_met['Distance travelled to work'] = df_2011_dis_met['Distance travelled to work'].str.strip()


df_2021_dis_met['Distance travelled to work'] = df_2021_dis_met['Distance travelled to work'].replace('Not in employment or works mainly offshore, in no fixed place or outside the UK', 'Other')
df_2011_dis_met['Distance travelled to work'] = df_2011_dis_met['Distance travelled to work'].replace('Work mainly at or from home', 'Works mainly from home')
  

#Creating All Categories
# Sum 'Count' for each unique 'Geography' and 'Distance travelled to work' combination in the 2021 dataset
all_categories_2021 = df_2021_dis_met.groupby(['geography', 'Method of travel to work'])['Count'].sum().reset_index()

# Add a new column for 'Method of travel to work' with the value 'All categories'
all_categories_2021['Distance travelled to work'] = 'All categories'

# Append this new dataframe to the existing 2021 dataframe
df_2021_dis_met = pd.concat([df_2021_dis_met, all_categories_2021])

# Ensure the dataframe is sorted by geography and distance travelled to work (if necessary)
df_2021_dis_met = df_2021_dis_met.sort_values(by=['geography', 'Method of travel to work'])

# Unique methods of travel to work in 2011
unique_2011 = df_2011_dis_met[~df_2011_dis_met['Distance travelled to work'].isin(df_2021_dis_met['Distance travelled to work'])]['Distance travelled to work'].unique()

# Unique methods of travel to work in 2021
unique_2021 = df_2021_dis_met[~df_2021_dis_met['Distance travelled to work'].isin(df_2011_dis_met['Distance travelled to work'])]['Distance travelled to work'].unique()

print("Unique to 2011 dataset:")
print(unique_2011)

print("Unique to 2021 dataset:")
print(unique_2021)

check_all_categories(df_2011_dis_met,'Distance travelled to work')
check_all_categories(df_2021_dis_met,'Distance travelled to work')

#%% Cell 7 removing duplicate entries


print("Rows in 2011 after processing:", len(df_2011_dis_met))
print("Rows in 2021 after processing:", len(df_2021_dis_met))

# Check for duplicates
print("Duplicates in 2011:", df_2011_dis_met.duplicated().sum())
print("Duplicates in 2021:", df_2021_dis_met.duplicated().sum())

# Duplicate rows
duplicate_rows = df_2021_dis_met[df_2021_dis_met.duplicated(['geography', 'Method of travel to work', 'Distance travelled to work'], keep='first')]


all_categories_2021 = df_2021_dis_met[df_2021_dis_met['Method of travel to work'] == 'All categories']
print("Additional 'All categories' rows in 2021:", all_categories_2021.shape[0])

# Check if concatenation created duplicate entries
print("Check for unexpected duplicate rows after concatenation in 2021:", df_2021_dis_met[df_2021_dis_met.duplicated(['geography', 'Method of travel to work', 'Distance travelled to work'], keep=False)].shape[0])

# Remove duplicates in 2021 dataset
df_2021_dis_met = df_2021_dis_met.drop_duplicates()

# Check how many rows are there after removing duplicates
print("Rows in 2021 after removing duplicates:", df_2021_dis_met.shape[0])

# Verify that 'All categories' rows are not duplicates
df_2021_dis_met = df_2021_dis_met.drop_duplicates(subset=['geography', 'Method of travel to work', 'Distance travelled to work'])

# Recheck unexpected duplicates after potential resolution
print("Recheck for unexpected duplicate rows after attempting resolution in 2021:", df_2021_dis_met[df_2021_dis_met.duplicated(['geography', 'Method of travel to work', 'Distance travelled to work'], keep=False)].shape[0])

#%% Cell 8 combining 

df_2021_dis_met['date'] = '2021'

# A dictionary from df_2011_dis_met that maps 'geography' to 'geography code'
geography_code_map = df_2011_dis_met.set_index('geography')['geography code'].to_dict()

# Add a new 'geography code' column to df_2021_dis_met
df_2021_dis_met['geography code'] = df_2021_dis_met['geography'].map(geography_code_map)


# Combine the two dataframes vertically
df_1121_dis_met = pd.concat([df_2011_dis_met, df_2021_dis_met], ignore_index=True)

# Sorting df_1121_dis_met by 'geography', 'Method of travel to work', and 'Distance travelled to work'
df_1121_dis_met = df_1121_dis_met.sort_values(by=['geography', 'Method of travel to work', 'Distance travelled to work'])

# Reset the index after sorting for clean index values
df_1121_dis_met.reset_index(drop=True, inplace=True)

df_1121_dis_met.loc[df_1121_dis_met['geography'] == "Westminster,City of London", 'geography code'] = 'n/a'


                                                                                                    