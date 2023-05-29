import matplotlib.pyplot as plt
import pandas as pd
import xlrd
import seaborn as sns
import numpy as np
# ---------------------------------------------------------------------
# Step 1: Import the the Data_Set using Pandas (Data_Set_5.csv)

df = pd.read_csv('Data_Set_5.csv')
# ---------------------------------------------------------------------
# Step 2: Find the cause of death for length of region

var = df.groupby('Cause_of_Death').Length_of_Reign.sum()
fig = plt.figure(1)
var.plot(kind='bar')
# ---------------------------------------------------------------------
# Step 3: Find the cause of death for length of region

var = df.groupby(['Emperor','Cause_of_Death']).Length_of_Reign.sum()
var.unstack().plot(kind='bar',stacked=True,  color=['red','blue'], grid=False)
# ---------------------------------------------------------------------
# Step 4: Find the cause of death for length of region

fig=plt.figure(3)
sns.violinplot(df['Cause_of_Death'], df['Length_of_Reign'])
# ---------------------------------------------------------------------
# Step 5: Create a pie chart showing the fraction of all Roman Emperors that were assassinated.

fig=plt.figure(4)
var = df.groupby(['Cause_of_Death']).sum().stack()
temp = var.unstack()
type(temp)
Length_of_Reign = temp['Length_of_Reign']
labe = temp.index
plt.axis("equal")
plt.pie(Length_of_Reign, labels=labe, autopct="%1.1f%%")

plt.show()

