'''''
Exercise 3
Create a horizontal bar chart that compares the deadliest actors in Hollywood. Sort the actors by their kill count and label each bar with the corresponding actor's name.
Don't forget to label your axes!
For reference, here's the raw data:
'''''
import pandas as pd
import matplotlib.pyplot as plt

hollywood_actor_kills = pd.read_csv('actor_kill_counts.csv')
hollywood_actor_kills
actor_names = hollywood_actor_kills['Actor'].values
kill_counts = hollywood_actor_kills['Count'].values

