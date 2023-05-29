import matplotlib.pyplot as plt
import pandas as pd
import xlrd
import seaborn as sns
import numpy as np

# ---------------------------------------------------------------------
# Step 1: Import the the Data_Set using Pandas using the following URl
# http://www.randalolson.com/wp-content/uploads/percent-bachelors-degrees-women-usa.csv

gender_degree_data = pd.read_csv("http://www.randalolson.com/wp-content/uploads/percent-bachelors-degrees-women-usa.csv")

# ---------------------------------------------------------------------
# Step 2: Import the the Data_Set using Pandas (Data_Set_2.csv)

gender_degree_data = pd.read_csv("Data_Set_2.csv")

# ---------------------------------------------------------------------
# Step 3: Find the majors and list it as characters.

fig = plt.figure(figsize=(14,12))
majors = list(gender_degree_data)
# df.columns.tolist() Should work too

majors = ['Health Professions', 'Public Administration', 'Education', 'Psychology',
          'Foreign Languages', 'English', 'Communications and Journalism',
          'Art and Performance', 'Biology', 'Agriculture',
          'Social Sciences and History', 'Business', 'Math and Statistics',
          'Architecture', 'Physical Sciences', 'Computer Science',
          'Engineering']


# ---------------------------------------------------------------------
# Step 4: Use for loop an plot all the majors measures data.

for ind, column in enumerate(majors):
    plt.plot(gender_degree_data['Year'], gender_degree_data[majors[ind]], lw=2.5)
    y_pos = gender_degree_data[majors[ind]].values[-1] - 0.5
    if column == "Foreign Languages":
        y_pos += 0.5
    elif column == "English":
        y_pos -= 0.5
    elif column == "Communications\nand Journalism":
        y_pos += 0.75
    elif column == "Art and Performance":
        y_pos -= 0.25
    elif column == "Agriculture":
        y_pos += 1.25
    elif column == "Social Sciences and History":
        y_pos += 0.25
    elif column == "Business":
        y_pos -= 0.75
    elif column == "Math and Statistics":
        y_pos += 0.75
    elif column == "Architecture":
        y_pos -= 0.75
    elif column == "Computer Science":
        y_pos += 0.75
    elif column == "Engineering":
        y_pos -= 0.25
    plt.text(2011.5, y_pos, column, fontsize=14)


plt.ylim(0, 90)
plt.xlim(1968, 2014)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.title("Percentage of Bachelor's degrees conferred to women in the U.S.A. by major (1970-2012)", fontsize=17, ha= "center")
# ---------------------------------------------------------------------
# Step 5: Save your plot in a separate file.
plt.savefig("percent-bachelors-degrees-women-usa.png", bbox_inches="tight")
plt.show()

