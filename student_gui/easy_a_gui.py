"""
    1/19/23 --> created the main window and added comboboxes

    1/22/23 --> added checkboxes and radio buttons for extra options

    1/26/23 --> started pulling actual data from parser.py

    1/27/23 --> added UO logo image

    2/1/23  --> added ProfButton functionality
"""

# =================================================================== #
# necessary libraries
# =================================================================== #
from tkinter import *
from tkinter import messagebox,ttk
from parser import *
import os.path

# =================================================================== #
# global variables
# =================================================================== #

# list of department names
department_list = ["Biology", "Chemistry", "Computer and Information Sciences", "Human Physiology", "Mathematics", "Physics", "Psychology"]
# variable indicating whether graduate student instructors are shown
include_GS = 1 
# variable indicating whether to sort by professors or classes (0 is classes 1 is professors)
sort_by_prof = 0 
# variable indicating which type of graph to show (1 for % As 0 for % Ds/Fs)
type_of_graph_to_show = 1 

# =================================================================== #
# functions for the student GUI
# =================================================================== #
"""
These functions are called when the user selects an option or clicks a button.
"""

def search_button(event):
    departmentName = getDepartmentNames()[deptNamecombo.current()]
    classLevel = classLevelcombo.get()
    classNumber = classNumbercombo.get()
    messagebox.showinfo(
        title="Searching",
        message=f"Department: {departmentName}\nClass Level: {classLevel}\nClass Number: {classNumber}\nSort by Profs: {sort_by_prof}\nInclude GS: {include_GS}\nAs or Fs: {type_of_graph_to_show}"
    )
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
        current_department = getDepartmentNames()[deptNamecombo.current()]
        current_class_numbers = getClassNumbers(current_department)
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

# =================================================================== #
# main window configuration
# =================================================================== #

# window name
window = Tk(className=" Easy A")
# window size
window.geometry("325x480")
# remove ability to change window dimensions
window.resizable(False, False)
# set background color
window.config(bg="#007030")

# =================================================================== #
# UO logo image
# =================================================================== #

# check if UO logo image is donwloaded and available to use
if (os.path.isfile("uoo.png")):
    UOimage = PhotoImage(file="uoo.png")
    imageLabel = Label(image=UOimage, bg="#007030")
    imageLabel.place(x=-7, y=-10)

# =================================================================== #
# labels indicating what each combobox is for
# =================================================================== #

# department name label
label1 = Label(text="Department Name", font=("Helvetica 15 bold"), bg="#007030", fg="#FEE11A")
# class level label
label2 = Label(text="Class Level", font=("Helvetica 15 bold"), bg="#007030", fg="#FEE11A")
# class number label
label3 = Label(text="Class Number", font=("Helvetica 15 bold"), bg="#007030", fg="#FEE11A")

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
ProfButton = Checkbutton(text="Search by Professors",
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
GSButton = Checkbutton(text="Include GS Instructors",
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
R1 = Radiobutton(text="Show Percent As", 
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
R2 = Radiobutton(text="Show Percent Ds/Fs", 
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

# =================================================================== #
# the search button
# =================================================================== #
"""
The search button is what the user clicks to pull up the graphs they want to see.
"""
searchButton = Button(text="Search", 
    width=15, 
    font=("Helvetica 15 bold"), 
    bg="#FEE11A", 
    fg="#007030", 
    activebackground="#FEE11A", 
    activeforeground="#007030"
)

# =================================================================== #
# setting default values for widgets
# =================================================================== #
"""
These are the values initially displayed in the comboboxes, checkboxes, 
and radio buttons.
"""
deptNamecombo.set("Biology")
classLevelcombo.set("")
classNumbercombo.set("")
GSButton.select()
R1.select()
R2.deselect()

# =================================================================== #
# binding functions to comboboxes and search button
# =================================================================== #
"""
These tie the comboboxes and search button to the functions for the GUI.
"""
deptNamecombo.bind('<<ComboboxSelected>>', change_departemnt)
classLevelcombo.bind('<<ComboboxSelected>>', change_class_level)
classNumbercombo.bind("<<ComboboxSelected>>", change_class_numbers)
searchButton.bind("<Button-1>", search_button)

# =================================================================== #
# placing widgets
# =================================================================== #
"""
This is the placement of all the widgets including labels, comboboxes, 
buttons, and checkboxes.

These are all centered (automatically or manually) and placed in descending
order.
"""
label1.place(relx=.5, y=25, anchor=CENTER)
deptNamecombo.place(relx=.5, y=60, anchor=CENTER)
label2.place(relx=.5, y=105, anchor=CENTER)
classLevelcombo.place(relx=.5, y=140, anchor=CENTER)
label3.place(relx=.5, y=185, anchor=CENTER)
classNumbercombo.place(relx=.5, y=220, anchor=CENTER)
ProfButton.place(x=65, y=245)
GSButton.place(x=65, y=280)
R1.place(x=65, y=315)
R2.place(x=65, y=345)
searchButton.place(relx=.5, y=410, anchor=CENTER)

# =================================================================== #
# mainloop so window stays open
# =================================================================== #
window.mainloop()
