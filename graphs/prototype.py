"""
CS 422 Project 1 (EasyA)

Data Visulization using matplotlib
- Different graphs
    - Single Graph Broken out by instructor
        - Single class ("MATH 111")
        - Single Department ("MATH")
        - All classes at a certain level ("All MATH 100-level")
    - All classes within particular level in a department (See project handout)
    - All instructors vs Regular faculty
        - All instructors (default)
        - Regular faculty found in course catalog
    - Easy A vs Just pass (2 graphs)
        - Percent A's
        - Percent D's or F's
    - Option to show class count

How to achieve:
    - Can use flags (ie classCount, singleGraph_class, singleGraph_department, ... )

"""
import matplotlib.pyplot as plt

# get data from scraper
department = "MATH"
professors = ["Patel", "Wang", "Smith", "Garcia", "Smith"]
percent_a = [65, 45, 68, 20, 5]
percent_f = [5, 30, 20, 10, 20]

# Use if data isnt in a dictionary
# Create dictionary of professors and the percent of As given
temp = {}
for key in professors:
    for value in percent_a:
        temp[key] = value
        percent_a.remove(value)
        break
professor_a = dict(sorted(temp.items(), key=lambda item: item[1], reverse=True))
percent_a = list(professor_a.values())
print(professor_a)


temp = {}
for key in professors:
    for value in percent_f:
        temp[key] = value
        percent_f.remove(value)
        break
professor_f = dict(sorted(temp.items(), key=lambda item: item[1], reverse=True))
percent_f = list(professor_f.values())
#print(list(professor_f.values()))
print(percent_f)

# More data
positions = range(len(percent_a))

# First subplot
plt.subplot(1, 2, 1)
# Plot bar graph
plt.bar(positions, percent_a)
# replace x-axis label
plt.xticks(positions, list(professor_a.keys()))
# change title of graph
plt.title("Math 111")
# set x and y-axis title
plt.xlabel("Instructor")
plt.ylabel("% As")



# Second subplot
plt.subplot(1, 2, 2)
plt.bar(positions, percent_f)
# replace x-axis label
plt.xticks(positions, list(professor_f.keys()))
# change title of graph
plt.title("Math 111")
# set x and y-axis title
plt.xlabel("Instructor")
plt.ylabel("% Ds / Fs")

plt.show()
