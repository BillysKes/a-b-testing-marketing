

1. [Project Overview](#project-overview)
2. [Dataset Description](#dataset-description)
3. [Data preprocessing](#data-preprocessing)
4. [Exploratory Data Analysis (EDA)](#eda)
   1. [Summary Statistics](#summary-statistics)
   2. [Visualizations](#visualizations)
5. [Hypothesis Testing](#hypothesis-testing) 



# 1. Project Overview

This project aims to analyze the A/B test results, where this test was conducted for a marketing company to evaluate the success of a marketing campaign and determine the impact of advertisements on the sales. Specifically, the project aims to compare the conversion rates between those people who were exposed to advertisements and those who were exposed to Public Service Announcements and discover the effectiveness of the campaign, and finally aims to test the statistical significance of the results.

# 2. Dataset Description
The dataset contains the users id, how the person were exposed to the product(ad or psa), if the person was converted(did they bought the product or not), the amount of ads seen by person, the day in which the person saw the biggest amount of ads and finally, the hour of the day where the person saw the biggest amount of ads. You can find more information about the dataset here : https://www.kaggle.com/datasets/faviovaz/marketing-ab-testing/data

  
# Data preprocessing


## Missing values

```
missing values : 
 user id          0
test group       0
converted        0
total ads        0
most ads day     0
most ads hour    0
dtype: int64
```

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

        test group most ads day
count      588101       588101
unique          2            7
top            ad       Friday
freq       564577        92608

```


## Outliers
```
Q1 = df['total ads'].quantile(0.25)
Q3 = df['total ads'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers_df = df[(df['total ads'] < lower_bound) | (df['total ads'] > upper_bound)]
exit(outliers_df.sort_values(by='total ads', ascending=False) // 10% of data
```



![image](https://github.com/BillysKes/a-b-testing-marketing/assets/73298709/5af13758-6e2f-41d3-9edb-b7218b2486e9)

![image](https://github.com/BillysKes/a-b-testing-marketing/assets/73298709/386244cd-47e4-4fbf-a594-862c3cda1229)



![image](https://github.com/BillysKes/a-b-testing-marketing/assets/73298709/16fd85ea-9feb-49ae-8afe-daeb972342e4)



![image](https://github.com/BillysKes/a-b-testing-marketing/assets/73298709/636185ac-1af1-463f-a891-66af1c898a80)
