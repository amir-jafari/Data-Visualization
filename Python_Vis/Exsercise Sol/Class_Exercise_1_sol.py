import matplotlib.pyplot as plt
import pandas as pd
import xlrd
import seaborn as sns
import numpy as np

# ---------------------------------------------------------------------
# Step 1: Import the the Data using Pandas (Data_Set_1.xlsx)

df = pd.read_excel("Data_Set_1.xlsx", "Sheet1")
# ---------------------------------------------------------------------
# Comment: Plots in matplotlib reside within a figure object, use plt.figure to create new figure.
# Step2: Extract the Ages from the data set and plot the distribution.

fig = plt.figure(1)
plt.hist(df['Age'], bins=7)
plt.title('Age distribution')
plt.xlabel('Age')
plt.ylabel('#Employee')
# ---------------------------------------------------------------------
# Step3: Extract the Ages from the data set use boxplot to plot the Ages measures.

fig = plt.figure(2)
plt.boxplot(df['Age'])
# ---------------------------------------------------------------------
# Step4: Extract the Ages from the data set and find the relationship between Age and Gender.
# Comment: Use seaborn libraray and use the violinplot.

fig=plt.figure(3)
sns.violinplot(df['Age'], df['Gender'])

# ---------------------------------------------------------------------
# Step5:  Find the sum of sales by each group at gender level. Store them in the variable.
# Comment: Use pandas and use groupby method.
var = df.groupby('Gender').Sales.sum()
# ---------------------------------------------------------------------
# Step6:  Plot sum of sales by each group at gender level using bar plot.

fig = plt.figure(4)
plt.xlabel('Gender')
plt.ylabel('Sum of Sales')
plt.title("Gender wise Sum of Sales")
var.plot(kind='bar')
# ---------------------------------------------------------------------
# Step7:  Plot sum of sales by each group at BMI level using line plot.

var = df.groupby('BMI').Sales.sum()
fig = plt.figure(5)
plt.xlabel('BMI')
plt.ylabel('Sum of Sales')
plt.title("BMI wise Sum of Sales")
var.plot(kind='line')
# ---------------------------------------------------------------------
# Step8:  Plot sum of sales by each group and BMI level using bar plot (Stacked Bar plot).

var = df.groupby(['BMI','Gender']).Sales.sum()
var.unstack().plot(kind='bar',stacked=True,  color=['red','blue'], grid=False)
# ---------------------------------------------------------------------
# Step9:  Plot sum of sales by each group and BMI level using bar plot (UnStacked Bar plot).

var = df.groupby(['BMI','Gender']).Sales.sum()
var.unstack().plot(kind='bar',stacked=False,  color=['red','blue'], grid=False)
# ---------------------------------------------------------------------
# Step10:  Find the relationship between age and Sales.

fig = plt.figure(7)
plt.scatter(df['Age'],df['Sales'])
# ---------------------------------------------------------------------
# Step11:  Find the relationship between age and Sales and find a way to include income into this Relationship.
# Comment: Added third variable income as size of the bubble

fig = plt.figure(8)
plt.scatter(df['Age'], df['Sales'], s=df['Income'])

# ---------------------------------------------------------------------
# Step12:  Use pie chart to shows the Sales for each gender.

var = df.groupby(['Gender']).sum().stack()
temp = var.unstack()
type(temp)
Sales = temp['Sales']
Group_Gender = temp.index
plt.axis("equal")
plt.pie(Sales, labels=Group_Gender, autopct="%1.1f%%")
plt.title("Expenses")
plt.show()

