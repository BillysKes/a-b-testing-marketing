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

To ensure our visualizations accurately reflect the population intended for A/B testing, we first dynamically calculate the required sample size (99% confidence level, 3% margin of error) resulting in a sample size of 1,838 per group. 

<img width="1000" height="500" alt="Figure_1" src="https://github.com/user-attachments/assets/528d1c36-bba2-4ffd-a9a3-9f233930f688" />

*Distribution of total ads seen by users in the control (PSA) vs. test (Ad) groups. The distributions are fairly similar, with medians hovering around 12-13 ads.*

<img width="800" height="600" alt="Figure_2" src="https://github.com/user-attachments/assets/6c6f8945-c66d-4c7f-8af1-8996e7644b82" />

*Median amount of ads seen broken down by conversion status. Users who converted generally saw more ads/PSAs before purchasing compared to those who did not convert.*

## Conversion rates

Conversion rate is calculated by dividing the number of conversions by the total number of visitors within our statistically sized samples.

**In []:**
```python
print('Conversion rate in the control group (Sample): ', control_sample['converted'].mean())
print('Conversion rate in the test group (Sample): ', test_sample['converted'].mean())
```

**Out []:**
```text
Conversion rate in the control group (Sample):  0.02013057671381937
Conversion rate in the test group (Sample):  0.025027203482045703
```
While the conversion rate in the test group (~2.50%) is slightly higher than the control group (~2.01%), we must test this difference for statistical significance.

# 6. Hypothesis Testing

* **Null Hypothesis ($H_0$):** Showing ads has no significant effect on the number of purchases.
* **Alternative Hypothesis ($H_1$):** Showing ads has a significant effect on the number of purchases.

## The "Large N" Problem and Proper Sample Sizing
If we run a frequentist statistical test (like a Chi-Square) on the entire historical dataset of 588,000+ rows, the test becomes hyper-sensitive. At that volume, even a fraction of a percent difference will trigger a mathematically "significant" result (p-value near 0), which can lead to false confidence in a campaign that actually has negligible business impact. 

To prevent this, we calculate the required sample size first and sample our data accordingly before running the Chi-square test of independence.

**In []:**
```python
# 1. Dynamically calculate sample size
sample_size = calculate_sample_size(population_size, 0.99, 0.03)
print(f"Required sample size per group: {sample_size}")

# 2. Draw the samples and combine
test_sample = experimental_group.sample(n=sample_size, random_state=42)
control_sample = control_group.sample(n=sample_size, random_state=42)
sampled_df = pd.concat([control_sample, test_sample])

# 3. Run the Chi-Square test on the properly sized sample
contingency_table = pd.crosstab(sampled_df['test_group'], sampled_df['converted'])
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

print("\nContingency Table (Sampled Data):")
print(contingency_table)
print(f"Chi-square statistic: {chi2:.4f}")
print(f"P-value: {p_value:.4e}")

alpha = 0.05
if p_value < alpha:
    print("Reject the null hypothesis. There is a significant difference between the groups.")
else:
    print("Fail to reject the null hypothesis. There is no significant difference between the groups.")
```

**Out []:**
```text
Required sample size per group: 1838

Contingency Table (Sampled Data):
converted   False  True 
test_group              
ad           1792     46
psa          1801     37
Chi-square statistic: 0.7889
P-value: 3.7443e-01

Fail to reject the null hypothesis. There is no significant difference between the groups.
```

### **Business Conclusion**
By applying rigorous sample sizing rather than testing the entire historical database, the p-value sits at 0.37 (well above the 0.05 alpha threshold). We fail to reject the null hypothesis. 

**Insight:** Mathematically speaking, the advertisement campaign did not meaningfully outperform the baseline Public Service Announcement. The business should investigate the quality/targeting of the ad campaign before scaling ad spend further, as the slight lift in conversion is likely due to random chance rather than ad effectiveness.
