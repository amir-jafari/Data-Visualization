'''''
Exercise 1
Create a line plot showing the number of marriages and divorces per capita in the U.S. between 1867 and 2014. Label both of the lines and show the legend.
Don't forget to label your axes!

Exercise 2
Create a vertical bar chart comparing the number of marriages and divorces per capita in the U.S. between 1900, 1950, and 2000.
Don't forget to label your axes!
'''''

import pandas as pd

us_marriage_divorce_data = pd.read_csv('us-marriages-divorces-1867-2014.csv')
years = us_marriage_divorce_data['Year'].values
marriages_per_capita = us_marriage_divorce_data['Marriages_per_1000'].values
divorces_per_capita = us_marriage_divorce_data['Divorces_per_1000'].values


