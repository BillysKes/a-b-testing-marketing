

1. [Project Overview](#project-overview)
2. [Dataset Description](#dataset-description)
3. [Data preprocessing](#data-preprocessing)
4. [Summary Statistics](#summary-statistics)
5. [Visualizations](#visualizations)
6. [Hypothesis Testing](#hypothesis-testing) 



# 1. Project Overview

This project aims to analyze the A/B test results, where this test is conducted for a marketing company to evaluate the success of a marketing campaign and determine the impact of advertisements on the sales. Specifically, the project aims to compare the conversion rates between those people who were exposed to advertisements and those who were exposed to Public Service Announcements and discover the effectiveness of the campaign, and finally aims to test the statistical significance of the results.

# 2. Dataset Description
The dataset contains the users id, how the person were exposed to the product(ad or psa), if the person was converted(did they bought the product or not), the amount of ads seen by person, the day in which the person saw the biggest amount of ads and finally, the hour of the day where the person saw the biggest amount of ads. You can find more information about the dataset here : https://www.kaggle.com/datasets/faviovaz/marketing-ab-testing/data

  
# 3. Data preprocessing

```
df = df.drop('Unnamed: 0', axis=1)
df.rename(columns=lambda x: x.strip().replace(" ", "_"), inplace=True)
```

## Missing values
In []:
```
print('\nmissing values : \n', df.isna().sum())  # missing values detection
print('\nduplicates :\n', df[df.duplicated()])  # duplicates detection
```

out []:
```
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
```
Q1 = df['total ads'].quantile(0.25)
Q3 = df['total ads'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers_df = df[(df['total ads'] < lower_bound) | (df['total ads'] > upper_bound)]
exit(outliers_df.sort_values(by='total ads', ascending=False) // 10% of data
```
After detecting outliers in this particular variable, we decide to perform winsorization. In this way, we tranform the bottom 5% values to be equal to the value corresponding to the 5th percentile and the upper 5% of the values are set equal to the value corresponding to the 95th percentile.

```
WinsorizedArray = winsorize(df['total ads],(0.05,0.05))
df['total ads']=WinsorizedArray
```

# 4. Summary Statistics
```
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
After the winsorization of 'total ads' variable the statistic results are :
```
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
Standard deviation dropped significantly. Also, max value is now 88, compared to 20065, the previous value.

# 5. Visualizations



![image](https://github.com/BillysKes/a-b-testing-marketing/assets/73298709/5af13758-6e2f-41d3-9edb-b7218b2486e9)

The high majority of people were exposed to advertisements instead of Public Service Announcements

![image](https://github.com/BillysKes/a-b-testing-marketing/assets/73298709/386244cd-47e4-4fbf-a594-862c3cda1229)

Only a small portion of people end up buying the product

![image](https://github.com/BillysKes/a-b-testing-marketing/assets/73298709/16fd85ea-9feb-49ae-8afe-daeb972342e4)



![image](https://github.com/BillysKes/a-b-testing-marketing/assets/73298709/636185ac-1af1-463f-a891-66af1c898a80)

In this nested pie chart we observe that 96% of the people were exposed to advertisements(Ads) while only 4% were exposed to PSA. Also, we obverve in the inner chart that 2.5% of the 'Ad' people converted(bought the product) while the rest 'Ad' people didn't(93.5%). Also, we notice that almost all 'PSA' people didn't buy the product(3.9% compared to 0.1%). The conversion rate of people who viewed ads instead of PSAs, seem to have higher conversion rate, which means that campaign seem to be succesful.
## Conversion rates

Conversion rate is calculated by dividing the number of conversions by the total number of visitors. <br /> <br />
**In []:**
```python
control_group = df[df['test_group'] == 'psa']
experimental_group = df[df['test_group'] == 'ad']
print(control_group['converted'].mean()) # baseline conversion rate
print(experimental_group['converted'].mean())
```

**Out []:**
```
conversion rate for the control group :  0.01785410644448223
conversion rate for the test group : 0.025546559636683747
```
Observing the results we assume that the ad campaign is more successful because the conversion rate is higher compared to the control group.

# 6. Hypothesis Testing

Null Hypothesis ($H_0$): Showing ads has no significant effect on the number of purchases

Alternative Hypothesis ($H_1$): Showing ads has significant effect on the number of purchases

## Chi-squared test

**In []:**
```python
contingency_table = pd.crosstab(df['test group'], df['converted'])
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
```

**out []:**
```
converted    False  True 
test group               
ad          550154  14423
psa          23104    420
Chi-square statistic: 54.005823883685245
P-value: 1.9989623063390075e-13
Degrees of freedom: 1
Expected frequencies:
[[550327.71899045  14249.28100955]
 [ 22930.28100955    593.71899045]]
Reject the null hypothesis. There is a significant difference between the groups.
```

