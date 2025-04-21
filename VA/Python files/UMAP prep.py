#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 12 20:34:27 2024

@author: theorogers
"""
#%% Cell 1, importing data and packages
import pandas as pd
import umap.umap_ as umap
import matplotlib.pyplot as plt
import seaborn as sns


df_file_path = '/Users/theorogers/Desktop/Assessments/VA/data sets/Processed/Ready/df_1121_dis_in_change.xlsx'

df_change = pd.read_excel(df_file_path)


#%% Cell 2,

keep_cols = ['geography', 'date', 'Industry', 'geography code']

UMAP_cols = [col for col in df_change.columns if col not in keep_cols]

# Initialize UMAP
reducer = umap.UMAP()

# Fit and transform the features
embedding = reducer.fit_transform(df_change[UMAP_cols])

# Create a new DataFrame for the embedding
umap_df = pd.DataFrame(embedding, columns=['UMAP1', 'UMAP2'])

# Concatenate the preserved columns back to the UMAP results
umap_comb_df = pd.concat([df_change[keep_cols], umap_df], axis=1)

plt.figure(figsize=(10, 7))
sns.scatterplot(x='UMAP1', y='UMAP2', hue='Industry', data=umap_comb_df)
plt.title('UMAP Projection')
plt.show()

umap_comb_df.to_excel('df_1121_dis_in_change_UMAP.xlsx', index=False)