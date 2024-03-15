# a-b-testing-marketing





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


