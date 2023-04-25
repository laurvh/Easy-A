"""
Author: Zachary Brant
CS 422 Software Methodologies
EasyA

Development process:
1/19/23 --> created the main window and added comboboxes

1/22/23 --> added checkboxes and radio buttons for extra options

1/26/23 --> started pulling actual data from parser.py

1/27/23 --> added UO logo image

2/1/23  --> added ProfButton functionality

2/2/23  --> added comments explaining functionality

2/4/23  --> added info button and pop up window
"""

# =================================================================== #
# necessary libraries
# =================================================================== #
import tkinter as tk
from tkinter import ttk
import gradeDataParser as gdp
import course_grade_visualizer as graph
import os.path

# =================================================================== #
# global variables
# =================================================================== #

# list of department names
department_name_dict = {"BI":"Biology", "CH":"Chemistry", "CIS":"Computer and Information Sciences", "HPHY":"Human Physiology", "MATH":"Mathematics", "PHYS":"Physics", "PSY":"Psychology"}
department_list = []
for i in gdp.getDepartmentNames():
    if i in department_name_dict.keys():
        department_list.append(department_name_dict.get(i))
    else:
        department_list.append(i)
# variable indicating whether graduate student instructors are shown
include_GS = 1 
# variable indicating whether to sort by professors or classes (0 is classes 1 is professors)
sort_by_prof = 0 
# variable indicating which type of graph to show (1 for % As 0 for % Ds/Fs)
type_of_graph_to_show = 0 
# variable indicating whether or not to show the number of each class next to professors names
show_class_count = 0

# =================================================================== #
# functions for the student GUI
# =================================================================== #
"""
These functions are called when the user selects an option or clicks a button.
"""

def search_button():
    """
    This function changes the class level based on the user's selection.

    Input:
    - none

    Actions:
    - Updates the values in the "classNumbercombo" dropdown list
    - Resets the value of "classNumbercombo"
    - Calls the "change_class_numbers" function
    - Focuses on the "searchButton"

    Output:
    - None
    """
    departmentName = gdp.getDepartmentNames()[deptNamecombo.current()]
    classLevel = classLevelcombo.get()
    classNumber = classNumbercombo.get()
    if (classNumber != ""):
        graph.main(departmentName, None, classNumber, include_GS, not sort_by_prof, type_of_graph_to_show, show_class_count)
    elif (classLevel != ""):
        graph.main(departmentName, classLevel, None, include_GS, not sort_by_prof, type_of_graph_to_show, show_class_count)
    else:
        graph.main(departmentName, None, None, include_GS, not sort_by_prof, type_of_graph_to_show, show_class_count)
    return

def change_class_level(event):
    """
    This function changes the class level based on the user's selection.

    Input:
    - event: An event that triggers the function to run

    Actions:
    - Updates the values in the "classNumbercombo" dropdown list
    - Resets the value of "classNumbercombo"
    - Calls the "change_class_numbers" function
    - Focuses on the "searchButton"

    Output:
    - None
    """
    current_class_level = classLevelcombo.get()
    if (current_class_level == ""):
        classNumbercombo.config(values=[""])
    else:
        current_department = gdp.getDepartmentNames()[deptNamecombo.current()]
        current_class_numbers = gdp.getClassNumbers(current_department)
        current_class_numbers[int(current_class_level)].insert(0, "")
        classNumbercombo.config(value=current_class_numbers[int(current_class_level)])
    classNumbercombo.set("")
    change_class_numbers(event)
    searchButton.focus()
    return

def change_class_numbers(event):
    """
    This function changes the class numbers based on the user's selection.

    Input:
    - event: An event that triggers the function to run

    Actions:
    - If the current class number selected is empty:
        - Enables the "ProfButton"
        - Deselects the "ProfButton"
        - Sets the "sort_by_prof" global variable to 0
    - If the current class number selected is not empty:
        - Disables the "ProfButton"
        - Selects the "ProfButton"
        - Sets the "sort_by_prof" global variable to 1
    - Focuses on the "searchButton"

    Output:
    - None
    """
    global sort_by_prof
    current_class_number = classNumbercombo.get()
    if (current_class_number == ""):
        ProfButton.config(state="active")
        ProfButton.deselect()
        sort_by_prof = 0
    else:
        ProfButton.config(state="disabled")
        ProfButton.select()
        sort_by_prof = 1
    searchButton.focus()
    return

def change_departemnt(event):
    """
    This function changes the class numbers based on the user's selection of the department.

    Input:
    - event: An event that triggers the function to run

    Actions:
    - Sets the value of "classLevelcombo" to an empty string
    - Calls the "change_class_level" function

    Output:
    - None
    """
    classLevelcombo.set("")
    change_class_level(event)
    return

def change_graph_type():
    """
    Input: None

    Actions:
    - Toggles the global variable "type_of_graph_to_show" between 0 and 1

    Output:
    - None
    """
    global type_of_graph_to_show
    if type_of_graph_to_show:
        type_of_graph_to_show = 0
    else:
        type_of_graph_to_show = 1
    return

def change_GS():
    """
    Input: None

    Actions:
    - Toggles the global variable "include_GS" between 0 and 1

    Output:
    - None
    """
    global include_GS
    if include_GS:
        include_GS = 0
    else:
        include_GS = 1
    return

def change_prof():
    """
    Input: None

    Actions:
    - Toggles the global variable "sort_by_prof" between 0 and 1

    Output:
    - None
    """
    global sort_by_prof
    if sort_by_prof:
        sort_by_prof = 0
    else:
        sort_by_prof = 1
    return

def change_class_count():
    """
    Input: None

    Actions:
    - Toggles the global variable "show_class_count" between 0 and 1

    Output:
    - None
    """
    global show_class_count
    if show_class_count:
        show_class_count = 0
    else:
        show_class_count = 1
    return

# =================================================================== #
# main window configuration
# =================================================================== #

# window name
window = tk.Tk(className=" EasyA")
# window size
window.geometry("600x520")
# remove ability to change window dimensions
window.resizable(False, False)
# set background color
window.config(bg="#007030")

# =================================================================== #
# checking for and inserting images
# =================================================================== #

# check if UO logo image is donwloaded and available to use
if (os.path.isfile("images/uoo.png")):
    UOimage = tk.PhotoImage(file="images/uoo.png")
    imageLabel = tk.Label(image=UOimage, bg="#007030")
    imageLabel.place(x=9, y=5)
# check if puddles image is donwloaded and available to use
if (os.path.isfile("images/puddles.png")):
    puddlesimage = tk.PhotoImage(file="images/puddles.png")
    puddlesimageLabel = tk.Label(image=puddlesimage, bg="#007030")
    puddlesimageLabel.place(x=450, y=405)

# =================================================================== #
# labels indicating what each combobox is for
# =================================================================== #

# department name label
label1 = tk.Label(text="Department Name", font=("Helvetica 15 bold"), bg="#007030", fg="#FEE11A")
# class level label
label2 = tk.Label(text="Class Level", font=("Helvetica 15 bold"), bg="#007030", fg="#FEE11A")
# class number label
label3 = tk.Label(text="Class Number", font=("Helvetica 15 bold"), bg="#007030", fg="#FEE11A")

# =================================================================== #
# combobox selections
# =================================================================== #
"""
ComboBoxes here are the dropdown lists used to select department name, 
class level, and class number. 

They are all read only.
"""
deptNamecombo = ttk.Combobox(
    state="readonly",
    values=department_list,
    font=("Helvetica 15"),
    width=16
)
classLevelcombo = ttk.Combobox(
    state="readonly",
    values=["", "100", "200", "300", "400", "500", "600"],
    font=("Helvetica 15"),
    width=16
)
classNumbercombo = ttk.Combobox(
    state="readonly",
    values=[""],
    font=("Helvetica 15"),
    width=16
)

# =================================================================== #
# Selection boxes for extra options (include GS, sort by professors, show % As or % D/Fs)
# =================================================================== #
"""
These checkboxes, buttons, and radio buttons all have their colors
set to the UO colors and the font is slightly smaller than the 
labels and combo boxes.
"""
# checkbox indicating whether to sort by professor name or class number
# this is only available when a class number is not selected
# otherwise it will default to on.
ProfButton = tk.Checkbutton(text="Sort by Professors",
    onvalue=1,
    offvalue=0, 
    font=("Helvetica 12 bold"), 
    height=1,
    bg="#007030", 
    fg="#FEE11A", 
    selectcolor="#007030", 
    activebackground="#007030", 
    activeforeground="#FEE11A", 
    command=change_prof
)

# checkbox indicating whether to include graduate student instructors
GSButton = tk.Checkbutton(text="Include GS Instructors",
    onvalue=1,
    offvalue=0, 
    font=("Helvetica 12 bold"), 
    height=1,
    bg="#007030", 
    fg="#FEE11A", 
    selectcolor="#007030", 
    activebackground="#007030", 
    activeforeground="#FEE11A", 
    command=change_GS
)

# the radio buttons letting the user decide whther to display graphs
# showing % As or % Ds/Fs
R1 = tk.Radiobutton(text="Show Percent As", 
    value=0,
    font=("Helvetica 12 bold"), 
    height=1,
    bg="#007030", 
    fg="#FEE11A", 
    selectcolor="#007030", 
    activebackground="#007030", 
    activeforeground="#FEE11A", 
    command=change_graph_type
)
R2 = tk.Radiobutton(text="Show Percent Ds/Fs", 
    value=1,
    font=("Helvetica 12 bold"), 
    height=1,
    bg="#007030", 
    fg="#FEE11A", 
    selectcolor="#007030", 
    activebackground="#007030", 
    activeforeground="#FEE11A", 
    command=change_graph_type
)

# checkbox indicating whether to include class count number
ClassCountButton = tk.Checkbutton(text="Show Number of Classes",
    onvalue=1,
    offvalue=0, 
    font=("Helvetica 12 bold"), 
    height=1,
    bg="#007030", 
    fg="#FEE11A", 
    selectcolor="#007030", 
    activebackground="#007030", 
    activeforeground="#FEE11A", 
    command=change_class_count
)

# =================================================================== #
# the search button
# =================================================================== #
"""
The search button is what the user clicks to pull up the graphs they want to see.
"""
searchButton = tk.Button(text="Search", 
    width=15, 
    font=("Helvetica 15 bold"), 
    bg="#FEE11A", 
    fg="#007030", 
    activebackground="#FEE11A", 
    activeforeground="#007030", 
    command = search_button
)

# =================================================================== #
# setting default values for widgets
# =================================================================== #
"""
These are the values initially displayed in the comboboxes, checkboxes, 
and radio buttons.
"""
deptNamecombo.set(department_list[0])
classLevelcombo.set("")
classNumbercombo.set("")
GSButton.select()
R1.select()
R2.deselect()
ClassCountButton.deselect()

# =================================================================== #
# binding functions to comboboxes and search button
# =================================================================== #
"""
These tie the comboboxes and search button to the functions for the GUI.
"""
deptNamecombo.bind('<<ComboboxSelected>>', change_departemnt)
classLevelcombo.bind('<<ComboboxSelected>>', change_class_level)
classNumbercombo.bind("<<ComboboxSelected>>", change_class_numbers)

# =================================================================== #
# placing widgets
# =================================================================== #
"""
This is the placement of all the widgets including labels, comboboxes, 
buttons, and checkboxes.

These are all centered (automatically or manually) and placed in descending
order.
"""
label1.place(relx=.5, y=25, anchor=tk.CENTER)
deptNamecombo.place(relx=.5, y=60, anchor=tk.CENTER)
label2.place(relx=.5, y=105, anchor=tk.CENTER)
classLevelcombo.place(relx=.5, y=140, anchor=tk.CENTER)
label3.place(relx=.5, y=185, anchor=tk.CENTER)
classNumbercombo.place(relx=.5, y=220, anchor=tk.CENTER)
ProfButton.place(x=200, y=245)
GSButton.place(x=200, y=280)
R1.place(x=200, y=315)
R2.place(x=200, y=345)
ClassCountButton.place(x=200, y=375)
searchButton.place(relx=.5, y=445, anchor=tk.CENTER)

# =================================================================== #
# info button
# =================================================================== #

# function to make the pop up window containing data source and some other information
def open_popup():
    top = tk.Toplevel(window)
    top.title("Information")
    top.resizable(False, False)
    top.config(bg="#007030")
    tk.Label(top, text='If your class doesn\'t show up here, it means the data was redacted.\nOriginal data is from 2013-2016 UO classes. Public records request done by the Daily Emerald.\nDeveloped by: Alexa Roskowski, Katherine Smirnov, Lauren Van Horn, Ryan Heise, Zachary Brant', 
            font=("Helvetica 12 bold"), 
            bg="#007030", 
            fg="#FEE11A"
            ).pack()
    top.attributes('-topmost', True)

# the button which opens the information pop up
infoButton = tk.Button(text="Info", 
    width=4, 
    font=("Helvetica 10 bold"), 
    bg="#FEE11A", 
    fg="#007030", 
    activebackground="#FEE11A", 
    activeforeground="#007030", 
    command = open_popup
)

# placing the info button
infoButton.place(relx=.92, y=5)


# =================================================================== #
# mainloop so window stays open
# =================================================================== #
window.mainloop()
