import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import os
import shutil
import json

"""
Filename: adminInputGUI.py
Purpose: The purpose of this file is to fulfill the use case of an administrator obtaining new
    grade data and updating the file system to reflect the new data
    This file doesn't interact with the other files in the system but merely updates an
    existing file in the repository
Creation Date: January 19th, 2023
Authors: Lauren Van Horn, Katherine Smirnov
Modification Date: January 23rd, 2023 - improved upload_file() function for more robust use, LVH
    January 26th, 2023 - added comments to upload_file(), LVH
    January 30th, 2023 - added check_headers(filename) function, LVH
    January 31st, 2023 - added no_middle_init(filename) function, LVH
    February 1st, 2023 - added ParseJSFile(filepath) function, KS
    February 2nd, 2023 - added better documentation and comments and visuals to match stuGUI, LVH
    February 3rd, 2023 - added compareNames() function, KS
"""


def ParseJSFile(filepath):
    """ ParseJSFile(filepath: str):
        Takes in the file, 'filepath' and constructs it into a .js file that we can then pull data from
        - Parameters
            filepath is the name of the file that the user has uploaded (i.e. /Users/Lauren/Desktop/gradedata.js)
        - Input
            We are stripping the leading 'var groups = ' and trailing code IF it is there. If not
            we simply return and move on to the next step of validating the contents of the file
    """
    try:
        # Try to strip file of leading and trailing info
        f = open(filepath)
        # Read filepath and save in 'data'
        data = f.read()
        # Extract only the JSON data from the file by slicing
        # The data string from the character after the "="
        # To the character before the ";"
        croppedData = data[data.find("=") + 1: data.find(";")]
        f.close()
        # Update data contents
        data = json.loads(croppedData)
        with open(filepath, 'w') as f:
            # Write data to file using indent=4 for readability
            json.dump(data, f, indent=4)
    # If we don't find the extra lines in the .js file
    # Return and move on to next file Validation step
    except:
        return


def check_headers(filename):
    """ check_header(filenmae: str):
        Takes in the file, 'filename' and checks the headers are the expected headers
        - Parameters
            filename is the name of the file that the user has uploaded (i.e. /Users/Lauren/Desktop/gradedata.js)
        - Input
            We are checking to see if the headers match what the system is expecting
            it steps through each class for each term and checks the header description
        - Note
            The function will return an error if:
                the headers are not what are expected
                contents of file are not valid .js data
    """
    # Define the expected headers for the data file
    expected_headers = ['TERM_DESC', 'aprec', 'bprec', 'cprec', 'crn', 'dprec', 'fprec', 'instructor']
    try:
        # Open the file and call it f
        with open(filename) as f:
            # Read the contents of the file and store in data
            data = json.loads(f.read())

            # Iterate through each class (clas) in the data
            for clas in data:
                # iterate through each term (term) in the class
                for term in data[clas]:
                    # retrieve the headers of the current term
                    headers = list(term.keys())
                    # compare the headers with the expected headers
                    if headers != expected_headers:
                        # show an error message if the headers don't match
                        messagebox.showerror("Incorrect Headers",
                                             "Incorrect headers. Expected headers: {}".format(expected_headers))
                        # return False if the headers don't match
                        return False
        # return True if all headers match the expected headers
        return True
    except:
        # if the file doesn't contain valid JSON data, print an error message
        print("Error: The file does not contain valid JSON data.")
        return False


def correct_data(filename):
    """ correct_data(filename: str):
        Takes in the file, 'filename' and ensures that the data is actually correct
        - Parameters
            filepath is the name of the file that the user has uploaded (i.e. /Users/Lauren/Desktop/gradedata.js)
        - Input
            We are stepping through each class for each term and checking the contents are valid
        - Note
            Will not throw an error but will print out a statement letting the user know the
            data is invalid
    """
    with open(filename) as f:
        # Read the contents of the file and parse it as a JSON object
        data = json.loads(f.read())

        expected_headers = ['TERM_DESC', 'aprec', 'bprec', 'cprec', 'crn', 'dprec', 'fprec', 'instructor']
        season = ['Spring', 'Winter', 'Fall', 'Summer']

        # Loop through each class (clas) in the data
        for clas in data:
            # Loop through each term in the class
            for term in data[clas]:
                # Go through aprec, dprec, and fprec and ensure
                # the data is actually an integer and the correct amount
                if type(term['aprec']) != str:
                    print(clas, term, "Incorrect aprec type")
                elif not all(
                        (term['aprec'][i].isdigit() or term['aprec'][i] == '.') for i in range(len(term['aprec']))):
                    print(clas, term, "Incorrect aprec number")
                else:
                    if float(term['aprec']) < 0 or float(term['aprec']) > 100:
                        print(clas, term, "Incorrect aprec type")
                if ((type(term['dprec']) != str)):
                    print(clas, "Incorrect dprec type")
                elif not all(
                        (term['dprec'][i].isdigit() or term['dprec'][i] == '.') for i in range(len(term['dprec']))):
                    print(clas, term, "Incorrect dprec number")
                else:
                    if float(term['dprec']) < 0 or float(term['dprec']) > 100:
                        print(clas, term, "Incorrect dprec amount")
                if ((type(term['fprec']) != str)):
                    print(clas, term, "Incorrect fprec type")
                elif not all(
                        (term['fprec'][i].isdigit() or term['fprec'][i] == '.') for i in range(len(term['fprec']))):
                    print(clas, term, "Incorrect fprec number")
                else:
                    # Check fprec amount
                    if float(term['fprec']) < 0 or float(term['fprec']) > 100:
                        print(clas, term, "Incorrect fprec amount")
                if ((type(term['instructor']) != str)):
                    print(clas, term, "Incorrect Instructor name")


def no_middle_init(filename):
    """ no_middle_init(filename: str):
        Takes in the file, 'filename' and removes the middle initial/name from the Instructor
        if it exists
        - Parameters
            filepath is the name of the file that the user has uploaded (i.e. /Users/Lauren/Desktop/gradedata.js)
        - Input
            We are stepping through each class for each term and removing the middle
            initial or middle name if it exists and updating the file
        - Note
            We are doing this to ensure that the name conventions between the wayback
            machine and the new .js data matches and we can pull data properly
    """
    with open(filename) as f:
        # Read the contents of the file and parse it as a JSON object
        data = json.loads(f.read())

        # Loop through each class (clas) in the data
        for clas in data:
            # Loop through each term in the class
            for term in data[clas]:
                # Pull the instructor name from the current term
                instructor = term["instructor"]

                # If the instructor name is empty, continue to the next term
                if (instructor == ""):
                    continue
                else:
                    # Split the instructor name into last name and first name
                    lname, first_name = instructor.split(', ')
                    # Split the first name into first name and middle name if it exists
                    if len(first_name.split(" ")) >= 2:
                        fname, *middle = first_name.split(" ")
                        # If the first name is abbreviated (ie. J. Craig Appleseed),
                        # Use the middle name as the first name instead
                        if "." in fname:
                            fname = middle[0]
                        # Update the instructor name in the term
                        # With the format lastname, firstname
                        term["instructor"] = "{}, {}".format(lname, fname)

    # Write the updated data back to the file
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def getProfessors(department: str) -> list:
    """ getProfessors(department: str) -> list
        Provides all the professors of the given department
        Input: department name (i.e. MATH)
        Output: returns a list of professors under a class name of such department from 'gd.js'
        Note: if inserted an invalid department name, will return an empty list
    """
    # Reads 'gd.js'
    f = open('gd.js', 'r')
    # Data holds a dictionary of 'gd.js'
    data = json.load(f)
    f.close()

    # Will hold list of all professors of a department
    returnVal = []

    # Iterates through all the class_names (i.e. MATH111)
    for class_name in data:
        # Index holds the start of the class number, to split between the department and the class number
        index = -1
        for i in range(len(class_name)):
            if class_name[i].isdigit():
                index = i
                break
        # Holds the department name of class_name
        dep = class_name[:index]
        # Checks if the inputed department name is the same as class_name
        if department == dep:
            # Iterates through class_name in 'gd.js'
            for term in data[class_name]:
                # Confirms not a duplicate instructor
                if term["instructor"] not in returnVal:
                    returnVal.append(term["instructor"])

    return returnVal


def compareNames() -> tuple:
    """ compareNames() -> tuple
        Compares the faculty names in 'Faculty.js' from 'gd.js'
        Output: Returns a tuple of the names matched and the names not matched
    """
    # Read Faculty data
    f_faculty = open('Faculty.js', 'r')

    # Faculty_data holds a dictionary from Faculty.js
    # Keys are the department names, values are the list of professors associated with such department
    faculty_data = json.load(f_faculty)
    f_faculty.close()

    # Counts the names from "Faculty.js" that are in "gd.js" (the reformatted names)
    common_facultyToGd = 0
    # Counts the names from "Faculty.js" that do not match
    noMatch_facultyToGd = 0

    # Iterates through departments
    for department in faculty_data:
        # "Neuroscience" is not a department name in the class names in 'gd.js'
        if department == "Neuroscience": continue

        # Professors in department in 'gd.js'
        gd_profs = getProfessors(department)

        # Iterates through professors from 'Faculty.js'
        for professor in faculty_data[department]:
            # Checks to see if professor in 'Faculty.js' is in 'gs.js'
            if professor in gd_profs:
                common_facultyToGd += 1
            else:
                noMatch_facultyToGd += 1
    return (common_facultyToGd, noMatch_facultyToGd)


def upload_file():
    """ upload_file():
        takes in no parameters but generates Admin GUI instructing user
        to upload a file of .js filetype. It then validates filetype, and expected headers,
        strips extra code, and removes middle initial of instructors to prep file for
        use by graphing functions
        - Note
            The file will return an error if:
                file extension is not of .js
                the headers are not what are expected
                contents of file are not valid .js data
                no file is selected
    """
    # Get the file path selected by the user using the filedialog module
    filepath = filedialog.askopenfilename()
    # Split the file path into the filename (filename) and file extension (file_extension)
    filename, file_extension = os.path.splitext(filepath)

    # Check if the file extension is not .js
    if file_extension != '.js':
        # Show an error message if the file extension is not .js
        messagebox.showerror("Invalid file type", "Please select a .js file.")
        return

    # Call the ParseJSFile function with the selected file path as the argument
    ParseJSFile(filepath)

    # Check if the headers of the file are incorrect
    if (check_headers(filepath) == False):
        return

    # Validate data value inputs
    correct_data(filepath)

    # Call the no_middle_init function to remove middle initials from instructor names
    no_middle_init(filepath)

    # Variable that keeps track of if we had to rename the file
    renamed = False
    # get the directory we're in
    destination_folder = os.getcwd()
    # Check if there's already a file in the filepath that's the same name
    if os.path.isfile(os.path.join(destination_folder, os.path.basename(filepath))):
        # Split between filename and file extension
        filename, file_extension = os.path.splitext(filepath)
        # Create new filename
        new_filename = f"{filename}(1){file_extension}"
        # if not os.path.isfile(os.path.join(destination_folder, new_filename)):
        #     break

        # Rename the file
        os.rename(filepath, os.path.join(destination_folder, new_filename))
        # Show that the file was renamed
        renamed = True

    # Remove the file named 'gd.js' gd.js is our main data repository
    os.remove("gd.js")
    # Check to make sure we didn't have to rename the file
    if renamed:
        shutil.move(new_filename, "gd.js")
    # Move the file to the current working directory and rename it to 'gd.js'
    else:
        shutil.move(filepath, "gd.js")

    # Check how many professors from the new data are also in Faculty.js
    (common_facultyToGd, noMatch_facultyToGd) = compareNames()

    # Prints the statistics found
    print(common_facultyToGd, "names were matched from Faculty.js to gd.js")
    print(noMatch_facultyToGd, "names were not matched from Faculty.js to gd.js")

    # Print a message indicating that the file has been uploaded and added to the directory
    print('File uploaded and added to directory.')


"""
The following lines of code set up Graphical User Interface for uploading new data
"""

# =================================================================== #
# main window configuration
# =================================================================== #

# window name
root = tk.Tk(className=" Easy A")
# window size
root.resizable(False, False)
# set background color
root.config(bg="#007030")

# Label 'instructions' that displays the text "Select a .js file to upload:"
instructions = tk.Label(root, text='Select a .js file to upload:',
                        font=("Helvetica 12 bold"),
                        bg="#007030",
                        fg="#FEE11A",
                        activebackground="#007030",
                        activeforeground="#FEE11A")
instructions.pack()

# label 'note' that displays a note about the expected headers of the file to be uploaded.
note = tk.Label(root, text='Note: The headers must be as follows, \n'
                           'TERM_DESC (term year), aprec, bprec, cprec, crn, '
                           'dprec, fprec, instructor (lname, fname)',
                font=("Helvetica 12 bold"),
                bg="#007030",
                fg="#FEE11A",
                activebackground="#007030",
                activeforeground="#FEE11A")
note.pack()

# button 'upload_button' that, when clicked, will trigger the upload_file() function
upload_button = tk.Button(root, text='Upload File', command=upload_file,
                          font=("Helvetica 15 bold"),
                          width=15,
                          bg="#FEE11A",
                          fg="#007030",
                          activebackground="#FEE11A",
                          activeforeground="#007030")
upload_button.pack()

# 'root.mainloop()' starts the event loop that will run the GUI until the user closes it.
root.mainloop()
