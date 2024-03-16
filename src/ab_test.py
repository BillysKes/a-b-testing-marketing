import math

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, norm


def cohen_d(group1, group2):
    mean_diff = np.mean(group1) - np.mean(group2)
    pooled_std = np.sqrt((np.std(group1, ddof=1)**2 + np.std(group2, ddof=1)**2) / 2)
    return mean_diff / pooled_std


def calculate_sample_size(population_size, confidence_level, margin_error, p=0.5):
    # Calculate Z-score
    z = norm.ppf(1 - (1 - confidence_level) / 2)
    # Calculate sample size
    n = (z ** 2 * p * (1 - p)) / (margin_error ** 2)
    # Adjust sample size for finite population
    n = n / (1 + ((n - 1) / population_size))
    return math.ceil(n)


df = pd.read_csv('C:\\Users\\Vasil\\Downloads\\winsorizedmarketing_AB.csv')

control_group = df[df['test_group'] == 'psa']
experimental_group = df[df['test_group'] == 'ad']

population_size = df.shape[0]
confidence_level = 0.99
margin_error = 0.03

sample_size = calculate_sample_size(population_size, confidence_level, margin_error)
print("Required sample size:", 10000)
test_sample = experimental_group.sample(n=10000)
control_sample = control_group.sample(n=10000)


contingency_table = pd.crosstab(df['test_group'], df['converted'])

chi2, p_value, dof, expected  = chi2_contingency(contingency_table)

print(contingency_table)
print("Chi-square statistic:", chi2)
print("P-value:", p_value)
print("Degrees of freedom:", dof)
print("Expected frequencies:")
print(expected)

alpha = 0.05
if p_value < alpha:
    print("Reject the null hypothesis. There is a significant difference between the groups.")
else:
    print("Fail to reject the null hypothesis. There is no significant difference between the groups.")


