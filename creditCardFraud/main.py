import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style='whitegrid',palette='cividis')

# Creating the dataframe
file_path = "./creditcard.csv"
df = pd.read_csv(file_path)

# dataset values
df.head()

# dataset statistical summary
df.describe()

# null values checking
print('Total of Null Values:', df.isnull().sum().max())

# checking the balance between legal and illegal transactions
fig, ax = plt.subplots(figsize=(5,5))
sns.countplot(x='Class',data=df);
print(pd.Series(df.Class).value_counts())
plt.show()

# checking outliers in `Amount` values
fig, ax = plt.subplots(figsize=(15, 3))
sns.boxplot(x='Amount', data=df)
plt.show()

# checking outlier values 
q1_amount = df.Amount.quantile(.25)
q3_amount = df.Amount.quantile(.75)
IQR_amount = q3_amount - q1_amount
print('IQR: ', IQR_amount)

# defining limits                                       
sup_amount = q3_amount + 1.5 * IQR_amount
inf_amount = q1_amount - 1.5 * IQR_amount

print('Upper limit: ', sup_amount)
print('Lower limit: ', inf_amount)


# cleaning the outliers in `Amount` values
df_clean = df.copy()
df_clean.drop(df_clean[df_clean.Amount>184.49].index, axis=0, inplace=True)

# new boxplot for `Amount` values
fig, ax = plt.subplots(figsize=(15, 3))
sns.boxplot(x='Amount', data=df_clean)
plt.show()

# legal transactions by time
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(x=(df_clean.Time[df_clean.Class==0]), bins=50);
ax.set_title('Legal Transactions by Time')
plt.show()