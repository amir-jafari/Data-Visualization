import matplotlib.pyplot as plt
import pandas as pd
import xlrd
import seaborn as sns
import numpy as np
# ---------------------------------------------------------------------
# Step 1: Import the the Data_Set using Pandas (Data_Set_6.csv)

df = pd.read_csv('Data_Set_6.csv')
arcade_revenue_cs_doctorates = pd.read_csv('Data_Set_6.csv')

# ---------------------------------------------------------------------
# Step 2: Extract data

arcade_revenue = arcade_revenue_cs_doctorates['Total Arcade Revenue (billions)'].values
cs_doctorates_awarded = arcade_revenue_cs_doctorates['Computer Science Doctorates Awarded (US)'].values
year= arcade_revenue_cs_doctorates['Year'].values
# ---------------------------------------------------------------------
# Step 3: Create a scatter plot showing the relationship between the total revenue earned by arcades and the number of Computer Science PhDs awarded in the U.S.
plt.figure(1)
plt.plot(year,arcade_revenue)

plt.figure(2)
plt.plot(year,cs_doctorates_awarded)

plt.figure(3)
plt.scatter(year,arcade_revenue,s=cs_doctorates_awarded)

plt.show()


