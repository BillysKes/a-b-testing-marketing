import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('C:\\Users\\Vasil\\Downloads\\winsorizedmarketing_AB.csv')

control_group = df[df['test group'] == 'psa']
experimental_group = df[df['test group'] == 'ad']
#print(control_group['converted'].mean())
control_convertRate = (control_group['converted'] == True).sum() / (len(control_group)) # baseline conversion rate
#exit(control_convertRate)
experimental_convertRate = (experimental_group['converted'] == True).sum() / (len(experimental_group))

'''plt.figure()
test_group_count = df.groupby('test group')['test group'].value_counts().reset_index()
plt.bar(test_group_count['test group'],test_group_count['count'], color=['blue','orange'])
plt.xlabel("test group")
plt.ylabel("count")
plt.title("Number of people who saw the advertisement vs who saw a PSA")

plt.figure()
converted_count = df.groupby('converted')['converted'].value_counts().reset_index()
plt.bar(converted_count['converted'].astype(str),converted_count['count'], color=['blue','orange'])
plt.xlabel("converted")
plt.ylabel("count")
plt.title("Number of people who bought the product vs who didn't")

plt.figure()
mostAdsDay_count = df.groupby('most ads day')['most ads day'].value_counts().reset_index()
plt.bar(mostAdsDay_count['most ads day'].astype(str),mostAdsDay_count['count'], color=['red','yellow','green','orange','purple','brown','black'])
plt.xlabel("day")
plt.ylabel("count")
plt.title("Total number of ads seen by people")
plt.figure()

inner = df.groupby(['test group','converted'])['converted'].value_counts()
inner_labels = inner.index.get_level_values(1)
outer = df.groupby('test group')['test group'].value_counts()
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
total_adsPSA=df.loc[df['test group'] == 'psa', 'total ads']
total_adsAd=df.loc[df['test group'] == 'ad', 'total ads']
plt.figure()
plt.boxplot(total_adsPSA)
plt.figure()
plt.boxplot(total_adsAd)

plt.show()
#print(df['test group'=='psa'])
# Calculate proportions


