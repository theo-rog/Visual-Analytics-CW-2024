#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 15:09:39 2024

@author: theorogers
"""
#%% Cell 1, importing and transposing data 
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN

path_file = "/Users/theorogers/Desktop/Assessments/VA/data sets/Processed/2 - 11CMLAD met dis pro.csv" 
df = pd.read_csv(path_file)

#%% Cell 2, PCA

#Removing/preserving the 'geographical code' column
df.set_index('geography', inplace=True)
geography_code_vector = df[['geography code']]
df_for_pca = df.drop('geography code', axis=1)
df_for_pca = df_for_pca.drop('date', axis=1)

#Remove all zero columns
df_for_pca = df_for_pca.loc[:, (df_for_pca != 0).all(axis=0)]



#Standardise the data
scaler = StandardScaler()
df_standardized = scaler.fit_transform(df_for_pca)

#Apply PCA
pca = PCA(n_components=3)
principal_components = pca.fit_transform(df_standardized)

pca_full = PCA()
pca_full.fit(df_standardized)

#Determine explained variance and explained variance ratio
explained_variance_ratio = pca_full.explained_variance_ratio_

#Find the number of components that explain at least 90% of the variance
cumulative_variance_ratio = np.cumsum(explained_variance_ratio)
n_components_90 = np.where(cumulative_variance_ratio >= 0.90)[0][0] + 1


#Create a scree plot
plt.figure(figsize=(10, 5))
plt.bar(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio, alpha=0.5, align='center',
        label='Individual explained variance')
plt.step(range(1, len(cumulative_variance_ratio) + 1), cumulative_variance_ratio, where='mid',
         label='Cumulative explained variance')
plt.axhline(y=0.90, color='r', linestyle='--', label='90% Explained Variance')
plt.axvline(x=n_components_90, color='r', linestyle='--', label=f'{n_components_90} Components')
plt.ylabel('Explained variance ratio', fontsize=16)
plt.xlabel('Principal component index', fontsize=16)
plt.title('Scree Plot', fontsize=20)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(loc='best', fontsize=16)
plt.tight_layout()
plt.show()

#Extract the principal components corresponding to the n_components_90
principal_components_90 = pca_full.transform(df_standardized)[:, :n_components_90]

#Update the column names for the new number of principal components
columns_names = ['PC' + str(i) for i in range(1, n_components_90 + 1)]
pca_df = pd.DataFrame(data=principal_components_90,
                      columns=columns_names,
                      index=df_for_pca.index)  # This ensures the index is preserved


#%% Cell 3, K-means
#K-means and visualising

#Run K-means clustering
kmeans = KMeans(n_clusters=3)
clusters = kmeans.fit_predict(pca_df)

#Plotting the PCA reduced data
plt.figure(figsize=(8, 6))
plt.scatter(pca_df['PC1'], pca_df['PC2'], c=clusters)
plt.title('PCA - Km Clusters', fontsize = 20)
plt.xlabel('Principal Component 1', fontsize = 16)
plt.ylabel('Principal Component 2', fontsize = 16)
plt.colorbar(label='Cluster')
plt.show()

pca_df['K means labels'] = clusters


buckinghamshire_index = pca_df.index.get_loc('Buckinghamshire')
buckinghamshire_cluster = pca_df.loc['Buckinghamshire', 'K means labels']

def assign_new_cluster(location):
    if location['K means labels'] == buckinghamshire_cluster:
        if location['PC2'] < -4:
            return 4
        else:
            return buckinghamshire_cluster 
    else:
        return location['K means labels']


pca_df['Adjusted K means labels'] = pca_df.apply(assign_new_cluster, axis=1)
alt_km_labels = pca_df['Adjusted K means labels']

# Plotting the PCA reduced data with cluster coloring
plt.figure(figsize=(8, 6))
plt.scatter(pca_df['PC1'], pca_df['PC2'], c=alt_km_labels)
plt.title('PCA - adjusted Km Clusters', fontsize = 20)
plt.xlabel('Principal Component 1', fontsize = 16)
plt.ylabel('Principal Component 2', fontsize = 16)
plt.colorbar(label='Adjusted K means labels')
plt.show()

pca_df = pca_df.drop('K means labels', axis=1)
pca_df = pca_df.drop('Adjusted K means labels', axis=1)


#%% Cell 4.1, DB-Scan prep

from sklearn.neighbors import NearestNeighbors

#The number of samples in a neighborhood for a point to be considered a core point
min_samples = 5

#Use NearestNeighbors to find the distance to the nearest min_samples points
nn = NearestNeighbors(n_neighbors=min_samples)
neighbors = nn.fit(df_standardized)
distances, indices = neighbors.kneighbors(df_standardized)

#Sort distances
sorted_distances = np.sort(distances[:, min_samples-1], axis=0)

#Plot the k-distance graph
plt.figure(figsize=(8, 4))
plt.plot(sorted_distances)
plt.ylabel('k-distance (eps)')
plt.xlabel('Points sorted by distance')
plt.title(f'k-distance Graph (k={min_samples})')
plt.show()

#Use the plot to pick a new value for eps (look for the elbow in the graph)


#%% Cell 4.2, DB-Scan

db = DBSCAN(eps=5, min_samples=10).fit(pca_df)


#Labels of the clusters
labels = db.labels_

#Number of clusters in labels, ignoring noise if present
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

#Print basic statistics
print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)

#Plot resulting clusters
plt.figure(figsize=(8, 6))

#The cluster labels are in `labels`; noise is labeled as `-1`

#Choose a subset of your principal components for visualization (e.g., PC1 and PC2)
plt.scatter(principal_components[:, 0], principal_components[:, 1], c=labels, s=50)
plt.title('DBSCAN Clustering')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')

#Add color bar to show the cluster labels
cbar = plt.colorbar()
cbar.set_label('Cluster Label')

plt.show()
#%% Cell 5, GMM
from sklearn.mixture import GaussianMixture

#Assuming you have your data stored in X

#Instantiate the GMM model with desired number of clusters
gmm = GaussianMixture(n_components=3)  # You can adjust the number of components as needed

#Fit the model to your data
gmm.fit(pca_df)

#Predict the cluster labels for your data
GMM_cluster_labels = gmm.predict(pca_df)

plt.figure(figsize=(8, 6))
plt.scatter(pca_df['PC1'], pca_df['PC2'], c=GMM_cluster_labels)
plt.title('PCA - GMM Clusters')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar(label='Cluster')
plt.show()

#%% Cell 6, Saving
pca_df['K means labels'] = clusters
pca_df['DBSCAN noise labels'] = labels
pca_df['DBSCAN labels'] = labels
pca_df['geography_code'] = geography_code_vector
pca_df['GMM Labels'] = GMM_cluster_labels
pca_df['Adjusted K means labels'] =alt_km_labels

pca_df.to_excel('/Users/theorogers/Desktop/Assessments/VisAn/data sets/Processed/2 - 11CMLAD met dis PCA4.xlsx',index=True)
