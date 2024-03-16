import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('C:\\Users\\Vasil\\Downloads\\winsorizedmarketing_AB.csv')


control_group = df[df['test_group'] == 'psa']
experimental_group = df[df['test_group'] == 'ad']
print('conversion rate in the control group : ',control_group['converted'].mean()) # baseline conversion rate
print('conversion rate in the test group :',experimental_group['converted'].mean())

'''plt.figure()
test_group_count = df.groupby('test_group')['test_group'].value_counts().reset_index()
plt.bar(test_group_count['test_group'],test_group_count['count'], color=['blue','orange'])
plt.xlabel("test_group")
plt.ylabel("count")
plt.title("Number of people who saw the advertisement vs who saw a PSA")

plt.figure()
converted_count = df.groupby('converted')['converted'].value_counts().reset_index()
plt.bar(converted_count['converted'].astype(str),converted_count['count'], color=['blue','orange'])
plt.xlabel("converted")
plt.ylabel("count")
plt.title("Number of people who bought the product vs who didn't")

plt.figure()
mostAdsDay_count = df.groupby('most_ads_day')['most_ads_day'].value_counts().reset_index()
plt.bar(mostAdsDay_count['most_ads_day'].astype(str),mostAdsDay_count['count'], color=['red','yellow','green','orange','purple','brown','black'])
plt.xlabel("day")
plt.ylabel("count")
plt.title("Total number of ads seen by people")
plt.figure()

inner = df.groupby(['test_group','converted'])['converted'].value_counts()
inner_labels = inner.index.get_level_values(1)
outer = df.groupby('test_group')['test_group'].value_counts()
print(inner)
print(outer)
fig, ax = plt.subplots(figsize=(24,12))
size = 0.3
ax.pie(outer.values.flatten(), radius=1,
       labels=outer.index,
       autopct='%1.1f%%',
       wedgeprops=dict(width=size, edgecolor='w'))

ax.pie(inner.values.flatten(), radius=1-size,
       labels = inner_labels,
autopct='%1.1f%%',
       wedgeprops=dict(width=size, edgecolor='w'))
ax.set(aspect="equal", title='Distribution of Converted by Test Group')
plt.show()'''

#totalAdsmedian=df.groupby('test group')['total ads'].mean()
#print(totalAdsmedian)
total_adsPSA=df.loc[df['test_group'] == 'psa', 'total_ads']
total_adsAd=df.loc[df['test_group'] == 'ad', 'total_ads']
plt.figure()
plt.boxplot(total_adsPSA)
plt.figure()
plt.boxplot(total_adsAd)

plt.show()
#print(df['test group'=='psa'])
# Calculate proportions


