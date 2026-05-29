import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import norm

# 1. Bring in the sampling logic so visualizations match the A/B test
def calculate_sample_size(population_size, confidence_level, margin_error, p=0.5):
    z = norm.ppf(1 - (1 - confidence_level) / 2)
    n = (z ** 2 * p * (1 - p)) / (margin_error ** 2)
    n = n / (1 + ((n - 1) / population_size))
    return math.ceil(n)

df = pd.read_csv('C:\\Users\\Vasil\\Downloads\\winsorizedmarketing_AB.csv')

control_group = df[df['test_group'] == 'psa']
experimental_group = df[df['test_group'] == 'ad']

population_size = df.shape[0]
sample_size = calculate_sample_size(population_size, 0.99, 0.03)

test_sample = experimental_group.sample(n=sample_size, random_state=42)
control_sample = control_group.sample(n=sample_size, random_state=42)
sampled_df = pd.concat([control_sample, test_sample])

print('Conversion rate in the control group (Sample): ', control_sample['converted'].mean())
print('Conversion rate in the test group (Sample): ', test_sample['converted'].mean())

# 2. Plot Boxplots side-by-side for clean comparison
total_adsPSA = control_sample['total_ads']
total_adsAd = test_sample['total_ads']

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
axes[0].boxplot(total_adsPSA)
axes[0].set_title('Total Ads Seen (PSA / Control)')
axes[0].set_ylabel('Amount of Ads')

axes[1].boxplot(total_adsAd)
axes[1].set_title('Total Ads Seen (Ad / Test)')

plt.tight_layout()
plt.show()

# 3. Bar chart for median ads seen by conversion status (using SAMPLED data)
avgTotalAdsgrouped = sampled_df.groupby(['test_group', 'converted'])['total_ads'].median().reset_index()

# Pivot the DataFrame to get the data in the right format for plotting
pivot_df = avgTotalAdsgrouped.pivot(index='test_group', columns='converted', values='total_ads')

# Plotting
pivot_df.plot(kind='bar', stacked=False, figsize=(8, 6))
plt.title('Amount of Ads Seen by Person (Median) - Sampled Data')
plt.xlabel('Test Group')
plt.ylabel('Amount')
plt.xticks(rotation=0)
plt.legend(title='Converted', labels=['False', 'True'])
plt.show()
