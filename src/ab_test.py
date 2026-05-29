import math
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, norm

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

# 1. Dynamically calculate and print the actual sample size
sample_size = calculate_sample_size(population_size, confidence_level, margin_error)
print(f"Required sample size per group: {sample_size}")

# 2. Draw the samples using the calculated size (added random_state for reproducibility)
test_sample = experimental_group.sample(n=sample_size, random_state=42)
control_sample = control_group.sample(n=sample_size, random_state=42)

# 3. Combine the samples into a single dataframe for testing
sampled_df = pd.concat([control_sample, test_sample])

# 4. Run the crosstab on the SAMPLED data, not the global dataset
contingency_table = pd.crosstab(sampled_df['test_group'], sampled_df['converted'])

chi2, p_value, dof, expected = chi2_contingency(contingency_table)

print("\n--- A/B Test Results ---")
print("\nContingency Table (Sampled Data):")
print(contingency_table)
print(f"\nChi-square statistic: {chi2:.4f}")
print(f"P-value: {p_value:.4e}")
print(f"Degrees of freedom: {dof}")
print("\nExpected frequencies:")
print(np.round(expected, 2))

alpha = 0.05
print("\n--- Conclusion ---")
if p_value < alpha:
    print("Reject the null hypothesis. There is a significant difference between the groups.")
else:
    print("Fail to reject the null hypothesis. There is no significant difference between the groups.")
