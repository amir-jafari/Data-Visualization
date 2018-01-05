import matplotlib.pyplot as plt
import pandas as pd
import xlrd
import seaborn as sns
import numpy as np

df=pd.read_excel("First.xlsx", "Sheet1")


fig=plt.figure(1) #Plots in matplotlib reside within a figure object, use plt.figure to create new figure
#Create one or more subplots using add_subplot, because you can't create blank figure
ax = fig.add_subplot(1,1,1)
#Variable
ax.hist(df['Age'],bins = 7) # Here you can play with number of bins Labels and Tit
plt.title('Age distribution')
plt.xlabel('Age')
plt.ylabel('#Employee')


fig=plt.figure(2)
ax = fig.add_subplot(1,1,1)
#Variable
ax.boxplot(df['Age'])

ax.boxplot(df['Age'])

#data_to_plot = [df['Age'], df['Income']]
#ax.boxplot(data_to_plot)

fig=plt.figure(3)
sns.violinplot(df['Age'], df['BMI']) #Variable Plot

sns.despine()


var = df.groupby('Gender').Sales.sum() #grouped sum of sales at Gender level

fig = plt.figure(4)
ax1 = fig.add_subplot(1,1,1)
ax1.set_xlabel('Gender')
ax1.set_ylabel('Sum of Sales')
ax1.set_title("Gender wise Sum of Sales")
var.plot(kind='bar')

var = df.groupby('BMI').Sales.sum()
fig = plt.figure(5)
ax1 = fig.add_subplot(1,1,1)
ax1.set_xlabel('BMI')
ax1.set_ylabel('Sum of Sales')
ax1.set_title("BMI wise Sum of Sales")
var.plot(kind='line')


var = df.groupby(['BMI','Gender']).Sales.sum()
var.unstack().plot(kind='bar',stacked=False,  color=['red','blue'], grid=False)

fig = plt.figure(7)
ax = fig.add_subplot(1,1,1)
ax.scatter(df['Age'],df['Sales']) #You can also add more variables here to represent color and size.

fig = plt.figure(8)
ax = fig.add_subplot(1,1,1)
ax.scatter(df['Age'],df['Sales'], s=df['Income']) # Added third variable income as size of the bubble
plt.show()
var=df.groupby(['Gender']).sum().stack()
temp=var.unstack()
type(temp)
x_list = temp['Sales']
label_list = temp.index
plt.axis("equal") #The pie chart is oval by default. To make it a circle use pyplot.axis("equal")
#To show the percentage of each pie slice, pass an output format to the autopctparameter
plt.pie(x_list,labels=label_list,autopct="%1.1f%%")
plt.title("Pastafarianism expenses")


#Generate a random number, you can refer your data values also
data = np.random.rand(4,2)
rows = list('1234') #rows categories
columns = list('MF') #column categories
fig,ax=plt.subplots()
#Advance color controls
ax.pcolor(data,cmap=plt.cm.Reds,edgecolors='k')
ax.set_xticks(np.arange(0,2)+0.5)
ax.set_yticks(np.arange(0,4)+0.5)
# Here we position the tick labels for x and y axis
ax.xaxis.tick_bottom()
ax.yaxis.tick_left()
#Values against each labels
ax.set_xticklabels(columns,minor=False,fontsize=20)
ax.set_yticklabels(rows,minor=False,fontsize=20)


plt.show()