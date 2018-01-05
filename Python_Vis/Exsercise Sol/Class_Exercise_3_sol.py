import matplotlib.pyplot as plt
import pandas as pd
import xlrd
import seaborn as sns
import numpy as np

# ---------------------------------------------------------------------
# Step 1: Import the the Data_Set using Pandas (Data_Set_3.csv)

us_marriage_divorce_data = pd.read_csv('Data_Set_3.csv')
# ---------------------------------------------------------------------
# Step 2: Extract each variable into separate dummy variables

years = us_marriage_divorce_data['Year'].values
marriages_per_capita = us_marriage_divorce_data['Marriages_per_1000'].values
marriages_per_capita_cor = marriages_per_capita[~np.isnan(marriages_per_capita)]

divorces_per_capita = us_marriage_divorce_data['Divorces_per_1000'].values
divorces_per_capita_cor = divorces_per_capita[~np.isnan(divorces_per_capita)]

marriages = us_marriage_divorce_data['Marriages'].values
marriages_cor = marriages[~np.isnan(marriages)]

divorces = us_marriage_divorce_data['Divorces'].values
divorces_cor = divorces [~np.isnan(divorces )]

population = us_marriage_divorce_data['Population'].values
population_cor = population [~np.isnan(population )]
# ---------------------------------------------------------------------
# Step 3: Create a line plot showing the number of marriages and divorces per capita in the U.S. between 1867 and 2014.

plt.figure(1)
plt.plot(years,marriages_per_capita)
# ---------------------------------------------------------------------
# Step 4: Label both of the lines and show the legend.
#Comment :Don't forget to label your axes!

plt.figure(2)
plt.plot(years,marriages_per_capita)
plt.xlabel('Years')
plt.ylabel('Marriage')
plt.title('Marriage per capita')

# ---------------------------------------------------------------------
# Step 5: Label both of the lines and show the legend.

plt.figure(3)
plt.plot(years,divorces_per_capita)
plt.xlabel('Years')
plt.ylabel('Divorce')
plt.title('Divorce per capita')

# ---------------------------------------------------------------------
# Step 6: Compare marriage and divorce over time. Show the legends

fig, ax = plt.subplots()
plt.figure(4)
ax.plot(years,marriages_per_capita, label='marriages_per_capita')
ax.plot( years,divorces_per_capita, label='marriages_per_capita')
plt.legend(loc='lower right')
# ---------------------------------------------------------------------
# Step 7: Estimate the distribution of Marriages and Divorces over time

fig, ax = plt.subplots()
plt.figure(5)
ax.hist(divorces_per_capita_cor, bins=10)


fig, ax = plt.subplots()
plt.figure(6)
ax.hist(marriages_per_capita_cor, bins=10)
# ---------------------------------------------------------------------
# Step 7: Find the relationship between the Marriages and Divorces over time with population size

fig=plt.figure(7)
plt.plot(population, marriages)

fig=plt.figure(8)
plt.scatter(years, marriages_per_capita, s=population/1000000)


fig=plt.figure(9)
plt.plot(population, divorces)

fig=plt.figure(10)
plt.scatter(years, divorces_per_capita, s=population/1000000)
plt.show()








