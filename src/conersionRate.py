

import numpy as np
import pandas as pd
from scipy.stats._mstats_basic import winsorize
from matplotlib import pyplot as plt


pd.set_option('display.max_columns', None)  #
pd.set_option('display.width', None)  # fit more columns
df = pd.read_csv('C:\\Users\\Vasil\\Downloads\\marketing_AB.csv')

print(df.head())
df = df.drop('Unnamed: 0', axis=1)
df.rename(columns=lambda x: x.strip().replace(" ", "_"), inplace=True)

print('\ndata types : \n', df.dtypes)  # verifying that data types are all correct
print('\nmissing values : \n', df.isna().sum())  # missing values detection
print('\nduplicates :\n', df[df.duplicated()])  # duplicates detection

for column in df.columns:
    print("Column:", column)
    print(df[column].unique())
print("\n\n", round(df.describe(), 2))  # statistics information
print("\n median :\n",df.median(numeric_only=True))
print('\n\n', df.describe(include=['object', bool]))  # statistics for categorical variables

Q1 = df['total_ads'].quantile(0.25)
Q3 = df['total_ads'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers_df = df[(df['total_ads'] < lower_bound) | (df['total_ads'] > upper_bound)]
WinsorizedArray = winsorize(df['total_ads'],(0.05,0.05))
df['total_ads'] = WinsorizedArray

print(df['most_ads_day'].unique())
print(df['total_ads'].describe())
df.to_csv('C:\\Users\\vasil\\Downloads\\winsorizedmarketing_AB.csv', index=False)
#exit(outliers_df.sort_values(by='total ads', ascending=False).head(125))

control_group = df[df['test_group'] == 'psa']
experimental_group = df[df['test_group'] == 'ad']

control_convertRate = (control_group['converted'] == True).sum() / (len(control_group))
experimental_convertRate = (experimental_group['converted'] == True).sum() / (len(experimental_group))





