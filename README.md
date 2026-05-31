# 1. Project Overview

This project aims to analyze the A/B test results conducted for a marketing company to evaluate the success of a marketing campaign and determine the impact of advertisements on sales. Specifically, the project compares the conversion rates between people exposed to advertisements and those exposed to Public Service Announcements (PSAs). By calculating the appropriate statistical sample size, the project rigorously tests the statistical significance of the campaign's effectiveness while avoiding the pitfalls of over-sampling.

# 2. Dataset Description
The dataset contains the user ID, how the person was exposed to the product (ad or psa), if the person converted (bought the product or not), the amount of ads seen per person, the day on which the person saw the biggest amount of ads, and finally, the hour of the day when the person saw the biggest amount of ads. You can find more information about the dataset here: https://www.kaggle.com/datasets/faviovaz/marketing-ab-testing/data

# 3. Data preprocessing

```python
df = df.drop('Unnamed: 0', axis=1)
df.rename(columns=lambda x: x.strip().replace(" ", "_"), inplace=True)
```

## Missing values
**In []:**
```python
print('\nmissing values : \n', df.isna().sum())  # missing values detection
print('\nduplicates :\n', df[df.duplicated()])  # duplicates detection
```

**Out []:**
```text
missing values : 
 user id         0
test group       0
converted        0
total ads        0
most ads day     0
most ads hour    0
dtype: int64
```
There aren't any missing values, neither duplicate rows.

## Outliers detection
```python
Q1 = df['total ads'].quantile(0.25)
Q3 = df['total ads'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers_df = df[(df['total ads'] < lower_bound) | (df['total ads'] > upper_bound)]
exit(outliers_df.sort_values(by='total ads', ascending=False)) // 10% of data
```
After detecting outliers in this particular variable, we decide to perform winsorization. In this way, we transform the bottom 5% values to be equal to the value corresponding to the 5th percentile and the upper 5% of the values are set equal to the value corresponding to the 95th percentile.

```python
WinsorizedArray = winsorize(df['total ads'],(0.05,0.05))
df['total ads']=WinsorizedArray
```

# 4. Summary Statistics
```text
           user id  total ads  most ads hour
count   588101.00  588101.00      588101.00
mean   1310692.22      24.82          14.47
std     202225.98      43.72           4.83
min     900000.00       1.00           0.00
25%    1143190.00       4.00          11.00
50%    1313725.00      13.00          14.00
75%    1484088.00      27.00          18.00
max    1654483.00    2065.00          23.00

        test group most ads day converted
count      588101       588101    588101
unique          2            7         2
top            ad       Friday     False
freq       564577        92608    573258
```
After the winsorization of the 'total ads' variable the statistic results are:
```text
count    588101.000000
mean         21.002814
std          23.281371
min           1.000000
25%           4.000000
50%          13.000000
75%          27.000000
max          88.000000
Name: total ads, dtype: float64
```
Standard deviation dropped significantly. Also, max value is now 88, compared to 2065, the previous value.

# 5. Visualizations

To ensure our visualizations and tests are statistically rigorous without falling prey to the "Large N" problem (where massive datasets trigger false positives), we dynamically calculate the required sample size using a Power Analysis.

Targeting an 80% statistical power, a 5% alpha, and a 20% relative Minimum Detectable Effect (MDE), the formula required roughly 23,700 users per group. Since our historical control group only contained 23,524 users, we implemented a safety check to cap the sample size at the maximum available pool (23,524 per group) to run our visualizations and tests.

<img width="1000" height="500" alt="Figure_1" src="https://github.com/user-attachments/assets/78fc504a-7bbb-4c18-9178-81211ff71881" />

*Distribution of total ads seen by users in the control (PSA) vs. test (Ad) groups. The distributions are fairly similar, with medians hovering around 12-13 ads.

<img width="800" height="600" alt="Figure_2" src="https://github.com/user-attachments/assets/46b389e0-1429-46a2-8bbb-ae11a0101266" />

*Median amount of ads seen broken down by conversion status. Users who converted generally saw more ads/PSAs before purchasing compared to those who did not convert.
## Conversion rates

Conversion rate is calculated by dividing the number of conversions by the total number of visitors within our statistically sized samples.

**In []:**
```python
print('Conversion rate in the control group (Sample): ', control_sample['converted'].mean())
print('Conversion rate in the test group (Sample): ', test_sample['converted'].mean())
```

**Out []:**
```text
Conversion rate in the control group (Sample):  0.01785410644448223
Conversion rate in the test group (Sample):  0.027078728107464718
```
The conversion rate in the test group (~2.71%) is noticeably higher than the control group (~1.79%). We will now rigorously test this difference for statistical significance.

# 6. Hypothesis Testing

* **Null Hypothesis ($H_0$):** Showing ads has no significant effect on the number of purchases.
* **Alternative Hypothesis ($H_1$):** Showing ads has a significant effect on the number of purchases.

## Power Analysis & Dynamic Sample Sizing
Rather than testing the entire dataset of 588,000+ rows (which makes frequentist tests hyper-sensitive to negligible effects), we calculate the required sample size first. We set a realistic goal: the Ad must perform at least 20% better than the PSA baseline to be considered a success.


**In []:**
```python
# 1. Calculate the actual baseline conversion rate from the control group
baseline_rate = control_group['converted'].mean()

# 2. Define Minimum Detectable Effect (MDE) - 20% relative lift
relative_mde = 0.20 
expected_rate = baseline_rate * (1 + relative_mde)

# 3. Calculate required sample size (80% Power, 5% Alpha)
calculated_sample_size = calculate_ab_sample_size(baseline_rate, expected_rate, alpha=0.05, power=0.80)

# 4. SAFETY CHECK: Cap sample size to available data if required size exceeds it
max_available = min(len(control_group), len(experimental_group))
sample_size = min(calculated_sample_size, max_available)

# Draw the samples and combine
test_sample = experimental_group.sample(n=sample_size, random_state=42)
control_sample = control_group.sample(n=sample_size, random_state=42)
sampled_df = pd.concat([control_sample, test_sample])

# Run the Chi-Square test on the properly sized sample
contingency_table = pd.crosstab(sampled_df['test_group'], sampled_df['converted'])
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

print("\nContingency Table (Sampled Data):")
print(contingency_table)
print(f"Chi-square statistic: {chi2:.4f}")
print(f"P-value: {p_value:.4e}")

alpha_test = 0.05
if p_value < alpha_test:
    print("Reject the null hypothesis. There is a significant difference between the groups.")
else:
    print("Fail to reject the null hypothesis. There is no significant difference between the groups.")
```

**Out []:**
```text
Dynamic Baseline Rate: 0.0179
Target Expected Rate (+20% MDE): 0.0214
Calculated required sample size: 23703
Warning: Required sample size exceeds available data in the smallest group.
Capping sample size to maximum available: 23524

--- A/B Test Results ---

Contingency Table (Sampled Data):
converted   False  True 
test_group              
ad          22887    637
psa         23104    420

Chi-square statistic: 45.1545
P-value: 1.8209e-11

--- Conclusion ---
Reject the null hypothesis. There is a significant difference between the groups.
```

### **Business Conclusion**
By applying a rigorous Power Analysis, we determined that we needed ~23,700 users to reliably detect a 20% lift in sales. Capping our test at the available 23,524 users per group, the test yielded a p-value of 1.82e-11, which is far below our 0.05 alpha threshold. We successfully reject the null hypothesis.

