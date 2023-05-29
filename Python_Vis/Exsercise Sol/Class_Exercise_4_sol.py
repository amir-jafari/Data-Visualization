import matplotlib.pyplot as plt
import pandas as pd
import xlrd
import seaborn as sns
import numpy as np
# ---------------------------------------------------------------------
# Step 1: Import the the Data_Set using Pandas (Data_Set_4.csv)

hollywood_actor_kills = pd.read_csv('Data_Set_4.csv')
# ---------------------------------------------------------------------
# Step 2: Extract each variable into separate dummy variables

actor_names = hollywood_actor_kills['Actor'].values
kill_counts = hollywood_actor_kills['Count'].values

# ---------------------------------------------------------------------
# Step 3: Create  bar chart that compares the deadliest actors in Hollywood.

plt.figure(figsize=(24,9))
plt.bar(range(len(kill_counts)), kill_counts, align='center')
plt.xticks(range(len(kill_counts)), actor_names, size='small')
# ---------------------------------------------------------------------
# Step 4:  Sort the actors by their kill count and label each bar with the corresponding actor's name.

plt.figure(figsize=(24,9))
index = sorted(range(len(kill_counts)), key=lambda k: kill_counts[k])
kill_counts_sort = np.sort(kill_counts)

plt.bar(range(len(kill_counts)), kill_counts_sort, align='center')
plt.xticks(range(len(kill_counts)), actor_names[index], size='small')

# ---------------------------------------------------------------------
# Step 5:  Sort the actors by their kill count and label each bar with the corresponding actor's name.

plt.figure(figsize=(24,9))
index = sorted(range(len(kill_counts)), key=lambda k: kill_counts[k])
index_r = np.flipud(index)

kill_counts_sort = np.sort(kill_counts)
kill_counts_sort_r = np.sort(kill_counts)[::-1]

plt.bar(range(len(kill_counts_sort_r)), kill_counts_sort_r, align='center')
plt.xticks(range(len(kill_counts_sort_r)), actor_names[index_r], size='small')
plt.show()


