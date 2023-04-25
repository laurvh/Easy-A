"""
    Name: gradeDataParser.py
    Created: 1/20/2023
    Author: Katherine Smirnov

    Provides the data needed for the Student UI and for the graph visualizer.
        Returns list of courses for a department for the easy_A_GUI.py course name dropdown. Provides a dropdown menu
            which restricts user to select only valid course and department names.
        Parses data from 'gd.js'. Used by course_grade_visualizer.py (which gets user input from easy_A_GUI.py) to pull the data
            which to be displayed in the graphs.

    Files:
        Reads from 'Faculty.js' and 'gd.js'

    Modifications:
        1/20/2023: Successfully loaded data using json to a dictionary format. Wrote getter functions (parseGradeData)
                    for course_grade_visualizer.py to load their data
        1/25/2023: Wrote getter functions (getClassNumbers, getDepartmentNames), for easy_A_GUI.py dropdown menu
        2/1/2023: Wrote getFacultyData(), which reads from 'Faculty.js'
        2/2/2023: Fixed bug in parseGradeData which pulled incorrect data for a specific department; Used to check
                    if class name starts with department, and now checks by separating between alphabet characters and
                    digits (ex: "CH" vs "CHN", CH would also pull classes from CHN).


"""
# to load the files
import json


def parseGradeData(department: str, number: str, professor: str):
    """ parseGradeData(department: str, number: str, professor: str):
        Pulls from 'gd.js' and returns the data from the parameters. Different inputs lead to different return values

        - Parameters
            Department is the letters/department of a class code (i.e. MATH)
            Number is the class number (i.e. 111)
            Professor is the teacher of the class in the format "LastName, First" (i.e. Hornof, Anthony)

        - Input
            The innermost dictionary is a dictionary of the format
            {"TERM_DESC": "", "aprec": "", "bprec": "","cprec": "","crn": "","dprec": "","fprec": "","instructor": {professor}

            (i) If a department, number and professor are provided, a list of the innermost dictionaries of all
                the terms from the provided professor and class name is returned.

            (ii) If a department and number are provided, and professor is set to None, a list of the innermost dictionaries of all
                the terms from the provided class name is returned.

            (iii) If only a department is provided, a dictionary of lists is returned, with the keys being the class name
                and the values being the lists from (ii)

            (iv) Returns an error if parameters are not in the format from i-iii listed above.

        Note: doesn't check if department, number, or professor is a valid, because the user is only able to pick from
              what is available from the GUI (which is only valid data)

        Used by course_grade_visualizer.py

    """
    f = open('gd.js')
    gradeData = json.load(f)    # reads the gd.js from a json file to a dictionary

    returnVal = []      # will hold return value

    if department and professor:    # inputs department, number, prof (i.e: MATH111 with Smith) -> return list of dicts
        for term in gradeData[department + number]: #iterates through class name of that specified
            if term["instructor"] == professor:
                returnVal.append(term)

    elif department and number:  # inputs specific class, (i.e: MATH111) -> returns a dictionary (of lists)
        returnVal = gradeData[department + number]
    elif department:  # inputs only department (i.e: MATH) -> returns a dictionary (of lists)
        returnVal = {}
        for clas in gradeData:  #iterates through class names
            index = -1      # will store the index of where the department name ends in the class name
                                # previously had done startswith(department), but some department names overlap (ex: CH, CHN)
                                # which would give invalid class data
            for i in range(len(clas)):
                if clas[i].isdigit():   #checks if character is a digit -> is the start of the department name
                    index = i
                    break

            if department == clas[0:index]:     #appends data of class if correct department
                returnVal[clas[index:]] = gradeData[clas]
    # invalid input
    else:
        raise Exception("Must supply a department, department and number, or department and number and professor")

    f.close()
    return returnVal


def getClassNumbers(department: str) -> dict:
    """ getClassNumbers(department)
        Output a dictionary of all the class numbers from a specified department. Pulls
        such data from 'gd.js'.

        Input: department is the letters/department of a class code (i.e. MATH)
        Output: Dictionary with the keys being the class level (i.e. 100, 200...) and the values being a
                list of all the class names of that level (i.e. 111, 121 ...)

        Note:
            Does not validate that the department exists, because the user should not be able to input an invalid
            department

        Used by easy_A_GUI.py
    """

    f = open('gd.js')
    gradeData = json.load(f)    #loads 'gd.js' to dictionary

    class_numbers = {}      # stores the class numbers for a department, and separates by level
    class_numbers[100] = []
    class_numbers[200] = []
    class_numbers[300] = []
    class_numbers[400] = []
    class_numbers[500] = []
    class_numbers[600] = []
    levels = ["1", "2", "3", "4", "5", "6"]

    #parses through classes in 'gd.js'
    for clas in gradeData:
        if department in clas:   #checks what level the class is
            for l in levels:
                if clas.startswith(department + l):
                    # with the full class name (i.e. MATH111)
                    # class_numbers[int(l + "00")].append(clas)

                    # with only class name (i.e. 111)
                    class_numbers[int(l + "00")].append(clas.strip(department))
                    break

    return class_numbers


def getDepartmentNames() -> list:
    """ getDepartmentNames()
        Returns a list of the natural sciences departments
        Used by: easy_A_GUI.py
    """
    return ["BI", "CH", "CIS", "HPHY", "MATH", "PHYS", "PSY"]


def getFacultyData(department: str):
    """ getFacultyData(department)
        Pulls from 'Faculty.js', and returns a list of faculty names from a given department. If no department is provided
        (set to None), a dictionary is return with the keys being the department name, and the values being the list
        of faculty names from such department

        Used by: course_grade_visualizer.py
    """
    with open('Faculty.js', 'r') as f:
        gradeData = json.load(f)    #loads Faculty.js as a dictionary
        f.close()
        if not department:  #if no department specified, return all data
            return gradeData
        else:
            return gradeData[department]
