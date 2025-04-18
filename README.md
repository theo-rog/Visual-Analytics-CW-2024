# Analysis of commuting patterns, changed by industry and location in England and Wales.

The following project uses census data to analyse changing pattterns in commuter behaviour in England and Wales, between 2011 and 2021. This is achieved through various justified visualisation techniques, following Munzner's taxonomy. The final visualisation is presented in 3 dashboards in Tableau and is supported by a full report.

The anaylsis is conducted on:
- Changes in commuter methods and distances
- Regional variation, across Lower Tier Local Authority (LTLA) districts
- Commuter pattern analysis by industry
- Trend anaylsis through clustering (K-means, DB-scan and GMMs)and dimensionality reduction (PCA and UMAP)

## Repository Structure

There are 2 files in this repository:

### VA/ (Final submission)
This is what was submitted to the university to be graded, containing:
- report.pdf - Full report outlining the project pipeline, visualisation choices, and insights
- Tableau files/ - Contains the tableau dashboards under one file
- Python files/ - Python scripts used for processing the data including dimensionality reduction
- Data/ - Cleaned datasets, as well as shape files required for the tableau visualisation

### Raw data/ (Source data)
This contains the original datasets sourced from the UK Office for National Statistics via Nomis. These files are included for transparency and reproducibility. The raw data files are named using a consistent format for clarity. Each filename follows the pattern: (number of variables) - (year)(geographic level) (variable description). For example, 1 - 11LAD met.csv refers to 2011 data at the Local Authority District level, showing method of travel.

The variables in question are abbrevated as follows:
- met - method of travel to work
- in - industry
- dis - distance travelled to work

## Python Overview

Scripts included in the Python files folder:
- 2011 met dis processing.py – Cleans the 2011 method of travel and distance data
- 2021 met dis processing.py – Cleans the 2021 method of travel and distance data
- PCA prep.py – Prepares cleaned data for principal component analysis
- UMAP prep.py – Prepares 2011–2021 change data for UMAP dimensionality reduction

### Libraries used:
- pandas
- numpy
- scikit-learn
- umap-learn
- matplotlib

## Data Summary

The original data was obtained from the UK Office for National Statistics (via Nomis). It includes commuting behaviour broken down by (LTLA), method of travel, distance travelled, and industry.

Cleaned datasets used in the project (in VA/Data) include:
•	2 - 11CMLAD met dis comb.csv – Cleaned 2011 commuting method and distance data
•	df_1121_dis_in_change.xlsx – Combined industry commuting data from 2011 and 2021
•	df_1121_dis_in_change_UMAP.xlsx – UMAP-ready data for industry-based analysis
•	shape files/ – Map files used for geospatial visualisations in Tableau

## Notes
•	This project was submitted as part of a Data Science visual analytics module (MSc)
•	The Tableau dashboard is included as-is; further edits are not possible due to lack of access to Tableau

## Contact

If you have questions or would like to know more, feel free to reach out via GitHub or LinkedIn (https://www.linkedin.com/in/theo-rogers-15ab4a225/).



  





  
