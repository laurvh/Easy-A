"""
    Name: webScraper.py
    Created: 1/16/2023
    Author: Katherine Smirnov

    Pulls the faculty data of University of Oregon's Catalog of 2014-2015 from the natural sciences departments,
    creates a dictionary with the keys being the department name, and the values being a list of faculty and imports
    it into 'Faculty.js'

    Notes:
        This program only needs to be called if 'Faculty.js' is not populated.
            The data from University of Oregon's Catalog of 2014-2015 will not change, so
            once the data is inserted, there is no need to call this program again.

        With Beautiful Soup, it is common for too many request be sent to this webpage, leading for the web request
            to not be fulfilled. If it was unsuccessful for a certain department, an error message is
            printed: "Couldn't pull {department}", and the associated error. No data would be written to 'Faculty.js'
            - Rerunning the program typically fixes this issue

    Resources used:
        Writes to 'Faculty.js'
        Requests from the department pages of University of Oregon's Catalog of 2014-2015 (from the WayBack Machine)

    Modifications:
        1/17/2023: Wrote parseFaculty() and getFaculty()
        1/26/2023: Wrote main function which would dump data into 'Faculty.js'
        1/30/2023: Reformatted names to remove middle names


"""
# to pull from the websites
import requests
# parse the webscraped data
from bs4 import BeautifulSoup
import json

def parseFaculty(URL: str) -> list:
    """     parseFaculty(URL: str) -> list
    Input: a URL from the wayback machine of a department from the University of Oregon's Catalog of 2014-2015.
    Output: a list of faculty names from the URL. Each faculty name (each index) is in the format: lastName, firstName.
        If a part of the name has a ".", it is treated as a middle name and is removed.

    Note for inputted URLs differing than from what is specified as above:
        The scraper pulls from the html of the page and searches from containers of name "facultytextcontainer"
        If no such container exists, this function will return an empty list
    """

    page = requests.get(URL)    #get the contents from URL
    soup = BeautifulSoup(page.text, "html.parser")

    #----- all faculty-----
    container = soup.find("div", {"id": "facultytextcontainer"})  # the faculty names are stored in facultytextcontainer
    lines = container.findAll("p")      # each individual faculty name is in a <p>

    # ---------doesn't include emeriti section of faculty------
    # text = page.text.split('Emeriti')
    # soup = BeautifulSoup(text[0], "html.parser")
    # container = soup.find("div", {"id": "facultytextcontainer"})
    # lines = container.findAll("p")

    professors = [] # will hold all the faculty names

    #------------iterates through each paragraph in webscraper--------------
    for line in lines:
        try:
            # each paragraph is the faculty name, ",", and info about the faculty
            name, _ = line.text.split(",", 1)   # name is the faculty name
        except:
            # line is not a person's name
            continue
        else:
            # -------------reformatting name without middle name------------------------
            splitname = name.split(" ")     #list of each name in full name
            cleanname = []      #will hold name without middle name

            for n in splitname:
                # removes middle name (always formatted as "X."), "Jr." suffixes, or edge cases (i.e: Brett "Brick")
                if ("." in n) or ('"' in n) or ('(' in n):
                    pass
                else:
                    cleanname.append(n)

            #---------------appends name to list in the format: "lastName, firstName"------------------
                #lastname: pulls the remaining indicies after 0 for cases of 2 word last names (i.e. Van Horn)
            professors.append(' '.join(cleanname[1:]) + ", " + cleanname[0])
            continue
    page.close()
    return professors


def getFaculty() -> dict:
    """     getFaculty() -> dict
    Output: a dictionary where the keys are the natural sciences (i.e. Biology), and the values are a list of faculty.
            Returns -1 if unsuccessful in pulling one of the departments

    This function calls parseFaculty, which pulls the faculty data.

    """
    #wayback machine sites for only the natural sciences
    sites = [("BI", "https://web.archive.org/web/20141107201402/http://catalog.uoregon.edu/arts_sciences/biology/#facultytext"),
             ("CH", "https://web.archive.org/web/20141107201414/http://catalog.uoregon.edu/arts_sciences/chemistry/#facultytext"),
             ("CIS",
              "https://web.archive.org/web/20141107201434/http://catalog.uoregon.edu/arts_sciences/computerandinfoscience/#facultytext"),
             ("Data science", "NA"),
             ("Earth sciences", "NA"),
             ("Multidisciplinary science", "NA"),
             ("HPHY",
              "https://web.archive.org/web/20140901091007/http://catalog.uoregon.edu/arts_sciences/humanphysiology/#facultytext"),
             ("MATH",
              "https://web.archive.org/web/20140901091007/http://catalog.uoregon.edu/arts_sciences/mathematics/#facultytext"),
             ("Neuroscience",
              "https://web.archive.org/web/20140901091007/http://catalog.uoregon.edu/arts_sciences/neuroscience/#facultytext"),
             ("PHYS", "https://web.archive.org/web/20140901091007/http://catalog.uoregon.edu/arts_sciences/physics/#facultytext"),
             ("PSY", "https://web.archive.org/web/20141101200122/http://catalog.uoregon.edu/arts_sciences/psychology/#facultytext")]

    professors = {}     #will hold the faculty for each department

    #----------------calls the scraper on all of the natural sciences---------------
    for subject, URL in sites:
        #for natural science departments that have no URL in wayback machine (these departments didn't exist in 2015)
        if URL == "NA": continue
        try:
            professors[subject] = parseFaculty(URL)
            print("Successfully pulled", subject)
            continue
        except Exception as e:
            # notifies if there is an error with the parseFaculty
            print("Couldn't pull", subject)
            print(e)
            return -1

    return professors


if __name__ == '__main__':
    # inserts the faculty data (which is pulled from getFaculty()) and writes it to Faculty.js as a json file

    data = getFaculty()     #dictionary of professor names
    #checks that there were no errors in pulling the data
    if data != -1:
        with open('Faculty.js', 'w') as f:
            print("Writing to 'Faculty.js'..................")
            json_object = json.dumps(data, indent=4)      #formats dictionary into json object
            f.write(json_object)    # puts data into 'Faculty.js'
            f.close()
            print("Webscraper was successful")
