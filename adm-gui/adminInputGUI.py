import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import os
import csv
import shutil
import json

def csv_to_js(filepath):
    # Open the .csv file and read its contents
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        data = list(csv.reader(csvfile))
    # Get the file name without the .csv extension
    filename, _ = os.path.splitext(filepath)
    # Create a new .js file with the same name
    with open(f"{filename}.js", 'w', encoding='utf-8') as jsfile:
        # Write the data to the .js file in the desired format
        jsfile.write("var data = " + str(data) + ";")

def check_headers(filepath):
    expected_headers = ['TERM_DESC', 'aprec', 'bprec', 'cprec', 'crn', 'dprec', 'fprec', 'instructer']
    with open(filepath) as f:
        data = json.load(f)
        headers = list(data[0].keys())
        if headers != expected_headers:
            messagebox.showerror("Incorrect headers. Expected headers: {}".format(expected_headers))
            return False
    return True


def upload_file():
    filepath = filedialog.askopenfilename()
    filename, file_extension = os.path.splitext(filepath)

    if file_extension not in ['.js', '.csv']:
        messagebox.showerror("Invalid file type", "Please select a .js or .csv file.")
        return

    if not filepath:
        print("No file selected.")
        return
    if (file_extension == '.js'):
        csv_to_js(filepath)
    if(check_headers(filepath) == False)
        return
    #need to check what path we want it to go to
    destination_folder = '/path/to/existing/directory'
    if os.path.isfile(os.path.join(destination_folder, os.path.basename(filepath))):
        filename, file_extension = os.path.splitext(filepath)
        i = 1
        while True:
            new_filename = f"{filename}({i}){file_extension}"
            if not os.path.isfile(os.path.join(destination_folder, new_filename)):
                break
            i += 1
        #will uncomment when I'm positive it will work
        #os.remove("gd.js")
        #shutil.move(filename, "gd.js")
        os.rename(filepath, os.path.join(destination_folder, new_filename))
    else:
        os.rename(filepath, os.path.join(destination_folder, os.path.basename(filepath)))
    print('File uploaded and added to directory.')


root = tk.Tk()

instructions = tk.Label(root, text='Select a .js or .csv file to upload:')
instructions.pack()

note = tk.Label(root, text='Note: The headers must be as follows, \n'
                           'TERM_DESC (term year), aprec, bprec, cprec, crn, '
                           'dprec, fprec, instructor (lname, fname)')
note.pack()

upload_button = tk.Button(root, text='Upload File', command=upload_file, padx=20, pady=10)
upload_button.pack()

root.mainloop()
