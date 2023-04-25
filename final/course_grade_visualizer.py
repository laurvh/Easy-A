'''
Authors: Ryan Heise, Alexa Roskowski
CS 422 Software Methodologies
EasyA

Development Process:
1/19 --> made an aper funct as proof of
	concept 

1/22 --> changed aper funct, so if same teacher
	taught more than one class, the average
	percent would be used

1/25 --> code pushed to github

1/26 --> started to pull from parser.py

1/26 --> added function to sort teacher data 
	(sort_dict_by_value)

1/28 --> added department_graph() with if ask for 
	whole department. Displays class level 

1/30 --> added graph_data() so we dont need to
	resuse old code

1/31 --> added all_class_graph() that graphs
	all classes within a department.

2/1 --> finalized project and created tests

2/1 --> added comments describing what functions do

'''

# Imports
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import gradeDataParser as p 

# Global var
fig_num = 1

def main(dep: str, level:str , classNum: str, allInstrucs: bool, list_dept_num: bool, display_d_f: bool = False, countClasses: bool = False):
	"""
	Summary: 
		- This function processes a query about course grades based on various 
		inputs. It uses parseGradeData function to get grade data and calls different 
		graph functions (all_class_graph, department_graph, instructor_graph) based on 
		the inputs to display the results.

	Input:
		- dep (str): name of the department
		- level (str): level of the class (100-600)
		- classNum (str): class number
		- allInstrucs (bool): display all instructors or just faculty
		- list_dept_num (bool): a flag to indicate if department number is displayed
		- display_d_f (bool): (optional) a flag to indicate if data is displayed in a full format, default is False
		- countClasses (bool): (optional) a flag to indicate if the number of classes is counted, default is False

	Return: 
		- None
	"""
	# Parse all classes in department
	if level == None and classNum == None:
		#we only have department name, go through all the classes
		data = p.parseGradeData(dep, None, None)
		if list_dept_num:
			department_graph(data, dep, level, display_d_f, allInstrucs, countClasses)
		else:
			all_class_graph(data, dep, display_d_f, allInstrucs, countClasses)

	# Parse level in department
	elif level != None and dep != None and classNum == None:
		# we have the level of the department
		allC = p.getClassNumbers(dep)
		# store necessary data in new variable so we can look up the class number
		data = allC[int(level)]
		if list_dept_num: # Create graph with department numbers
			department_graph(data, dep, level, display_d_f, allInstrucs, countClasses)
		else: # Create graph with instructor names
			# we have the level of the department
			dat = []
			for c in data:
				dat += p.parseGradeData(dep, c, None)
			#plug into grapher
			instructor_graph(dep + " " + f'{level}-level', dat, display_d_f, allInstrucs, countClasses)
 
	# Parse individual class
	elif classNum != None and dep != None and level == None:
		# we have department and class number
		#get data
		d = p.parseGradeData(dep, classNum, None)
		#plug into aPer
		instructor_graph(dep + classNum, d, display_d_f, allInstrucs, countClasses)
	# call to main had invalid data
	else:
		print("ERROR: Invalid querry")
		return

# ------------------------------------------------------------------
#				FUNCTIONAL REQUIREMENT GRAPHS
# ------------------------------------------------------------------
def all_class_graph(class_list, dep, display_d_f, allInstrucs, countClasses):
	"""
	Summary: 
		- Displays graph with all classes in a department where the y-axis 
		  is the professor name and x-axis is the average percentage they 
		  give. Graph similar to a2 in Project 1 Document
	Input:
		- class_list (dict) : dictionary provided by the json parser
		- dep (str) : name of the department you are graphing (ie. MATH, BI, CIS)
		- display_d_f (bool) : a flag to indicate if data is displayed in a full format
		- allInstrucs (bool) : display all instructors or just faculty
		- countClasses (bool) : a flag to indicate if the number of classes is counted

	Return: 
		- None
	"""
	# Create new variable to store data to graph
	# Will have the following format: 
		# {name: [aperc, d/fperc, num classes taught], name2: [...], ...}
	myDict = {}
	# Data provided by json parser is a list of dictionary elements
	for i in class_list:
		# Start looking at key/values in dictionary
		for j in class_list[i]:
			# Set up key for myDict
			lname = j['instructor'].split(',')[0].strip()
			fname = j['instructor'].split(',')[1].strip()
			full_name = fname + " " + lname

			# Check to make sure data is valid
			if j['aprec'].strip() == "":
				j['aprec'] = "0.0"
			if j['dprec'].strip() == "":
				j['aprec'] = "0.0"
			if j['fprec'].strip() == "":
				j['aprec'] = "0.0"

			# Setting values for myDict
			total_failing = float(j['dprec']) + float(j['fprec'])
			aprec = float(j['aprec'])

			# Teacher name is already in dictionary. Add values to it
			if full_name in myDict:
				myDict[full_name][0] += aprec 			# a percentage
				myDict[full_name][1] += total_failing 	# d/f percentage
				myDict[full_name][2] += 1 				# number of classes
			# first time this teacher has shown up (count is 1)
			else:
				# check if we want all instructors or just faculty 
				if not allInstrucs and (i['instructor']) in p.getFacultyData(dep):
					# just Faculty
					myDict[full_name] = [aprec, total_failing, 1]
				elif allInstrucs:
					# all instructors
					myDict[full_name] = [aprec, total_failing, 1]
	# Average values in myDict and then graph the data
	myDict = average_dict(myDict)
	graph_data(myDict, "Instructor", f'All {dep} Classes', display_d_f, countClasses)

def department_graph(class_list, dep, level, display_d_f, allInstrucs, countClasses):
	"""
	Summary: 
		- Displays graph with all classes in a specified level where the 
		  y-axis is the class level and x-axis is the average percentage 
		  they give. Graph similar to graph (b) in Project 1 Document
	Input:
		- class_list (dict) : dictionary provided by the json parser
		- dep (str) : Department of class (ie MATH, BI, CS)
		- level (str) : Level of class (ie 122, 314)
		- display_d_f (bool) : a flag to indicate if data is displayed in a full format
		- allInstrucs (bool) : display all instructors or just faculty
		- countClasses (bool) : a flag to indicate if the number of classes is counted

	Return: 
		- None
	"""
	# Create new variable to store data to graph
	# Will have the following format
	#	 mydict = {class_num_1: [aperc, d+fperc, number_of_classes], class_num_2: [...]}
	myDict = {}
	# Loop over the list of classes (i is the class number ie 314)
	for i in class_list:
		# get class data from parser so we can add to myDict
		class_data = p.parseGradeData(dep, i, None)
		for j in class_data:
			# Set up key for myDict
			lname = j['instructor'].split(',')[0].strip()
			fname = j['instructor'].split(',')[1].strip()
			full_name = fname + " " + lname

			# Check to make sure data is valid
			if j['aprec'].strip() == "":
				j['aprec'] = "0.0"
			if j['dprec'].strip() == "":
				j['aprec'] = "0.0"
			if j['fprec'].strip() == "":
				j['aprec'] = "0.0"

			# Set up values for myDict
			total_failing = float(j['dprec']) + float(j['fprec'])
			aprec = float(j['aprec'])

			# Teacher name is already in dictionary. Add values to it
			if i in myDict:
				myDict[i][0] += aprec 			# a percentage
				myDict[i][1] += total_failing 	# d/f percentage
				myDict[i][2] += 1 				# number of classes

			# first time this teacher has shown up (count is 1)
			else:
				# check if we want all instructors or just faculty 
				if not allInstrucs and (j['instructor']) in p.getFacultyData(dep):
					# just Faculty
					myDict[i] = [aprec, total_failing, 1]
				elif allInstrucs:
					# all instructors
					myDict[i] = [aprec, total_failing, 1]
	# Average values in myDict and then graph the data
	myDict = average_dict(myDict)
	# if level was not displayed we want to display all 'x' level classes as a graph
	if level != None:
		graph_data(myDict, "Classes", f'All {dep} {level}-level classes', display_d_f, countClasses)
	else:
		graph_data(myDict, "Classes", f'All {dep} Classes', display_d_f, countClasses)

def instructor_graph(class_name, data, display_d_f, allInstrucs, countClasses, ):
	"""
	Summary: 
		- Displays graph with all professors who teach a specified class 
		  number where the y-axis are the instructors and x-axis is the 
		  average percentage they give. Graph similar to graph (b) in 
		  Project 1 Document
	Input:
		- class_name (str) : Name of the class
		- data (dict) : Dictionary from the scraper
		- display_d_f (bool) : a flag to indicate if data is displayed in a full format
		- allInstrucs (bool) : display all instructors or just faculty
		- countClasses (bool) : a flag to indicate if the number of classes is counted

	Return: 
		- None
	"""
	# Create new variable to store data to graph
	# Will have the following format
	#	 mydict = {instructor: [aperc, d+fperc, number_of_classes], instructor2: [...], ...}
	myDict = {}
	# Loop through data provided by scraper
	for i in data:
		# Set up key for myDict
		lname = i['instructor'].split(',')[0].strip()
		fname = i['instructor'].split(',')[1].strip()
		full_name = fname + " " + lname

		# Check to make sure data is valid
		if i['aprec'].strip() == "":
			i['aprec'] = "0.0"
		if i['dprec'].strip() == "":
			i['aprec'] = "0.0"
		if i['fprec'].strip() == "":
			i['aprec'] = "0.0"

		# Set up values for myDict
		total_failing = float(i['dprec']) + float(i['fprec'])
		aprec = float(i['aprec'])

		# Teacher name is already in dictionary. Add values to it
		if full_name in myDict:
			# we have a teacher who has taught already
			# add to the count of classes taught
			myDict[full_name][2] += 1; 
			myDict[full_name][0] += aprec
			myDict[full_name][1] += total_failing

		# first time this teacher has shown up (count is 1)
		else:
			# check if we want all instructors or just faculty 
			if not allInstrucs and i['instructor'] in p.getFacultyData(''.join([i for i in class_name if not i.isdigit()])):
				# just Faculty
				myDict[full_name] = [aprec, total_failing, 1]
			elif allInstrucs:
				# all instructors
				myDict[full_name] = [aprec, total_failing, 1]
	# Average values in myDict and then graph the data
	myDict = average_dict(myDict)
	# if allInstrucs is true, we want to set the title to "All <CLASS> Instructors"
	if allInstrucs:
		graph_data(myDict, "Instructor", f'All {class_name} Instructors', display_d_f, countClasses)
	else: # else, just display the class name as the title
		graph_data(myDict, "Instructor", class_name, display_d_f, countClasses)
	
# ------------------------------------------------------------------
#						CREATE GRAPHS
# ------------------------------------------------------------------
def graph_data(myDict, x_label: str, title:str, display_d_f: bool, countClasses: bool):
	"""
	Summary: 
		- Graphs data using matplotlib
	Input:
		- myDict (dict) : dictionary containing data to graph
		- x_label (str) : label for x-axis
		- title (str) : title of the graph
		- display_d_f (bool) : a flag to indicate if data is displayed in a full format
		- countClasses (bool) : a flag to indicate if the number of classes is counted
	Return: 
		- a matplotlib graph using plt.show()
	"""
	global fig_num
	# Call helper function to sort dict in decreasing order
	sorted_a = sort_dict_by_value(myDict, key_func=lambda x: x[0])
	sorted_f = sort_dict_by_value(myDict, key_func=lambda x: x[1])

	#create lists, so mathplots is easier		
	a_data = []
	a_per = []
	f_data = []
	f_per = []

	#add how many classes this professors done to name 'a' grades
	for i in sorted_a:
		# Add number of classses to data 
		numClasses = " (" + str(myDict[i][2]) + ")"
		# if countClasses is true append string to instructor/class name and append to list
		a_data.append(i + (numClasses if countClasses else ''))
		a_per.append(myDict[i][0])
	#add how many classes this professors done to name for 'd/f' grades
	for j in sorted_f:
		# Add number of classses to data 
		numClasses = " (" + str(myDict[i][2]) + ")"
		# if countClasses is true append string to instructor/class name and append to list
		f_data.append(j + (numClasses if countClasses else ''))
		f_per.append(myDict[j][1])

	# Check if user wanted to display 2 graphs
	if display_d_f:
		if len(f_data) > 30: # if length larger than 30, create graph with scroll
			graph_w_scroll(f_data, f_per, title, x_label, "Percentage of D / F")
			return
		else:
			y_lable = "Percentage of D / F"
			# Create graph
			fig, ax = plt.subplots(figsize=(10,6), num=title + " | " + y_lable + f" | Figure {fig_num}")
			ax.bar(f_data, f_per)
			ax.set_xlabel(x_label)
			ax.set_ylabel(y_lable)
			ax.set_title(title)
			ax.tick_params(axis='x', labelsize=10, rotation=90)
			fig_num += 1
			# add height to the bars
			rect = ax.patches
			for rect, f_per in zip(rect, f_per):
				# set the height for the 'y' argument in ax.text()
				height = rect.get_height()
				if height >= 4: # Add white text if the height is >= 4
					ax.text(
			            rect.get_x() + rect.get_width() / 2,
			            height - 0.01,
			            round(float(f_per),1),
			            horizontalalignment='center',
			            verticalalignment='top',
			            color='White',
			            fontsize='small'
					)
				else: # else, set the text color to black
					ax.text(
			            rect.get_x() + rect.get_width() / 2,
			            height + 0.01,
			            round(float(f_per),1),
			            horizontalalignment='center',
			            verticalalignment='bottom',
			            color='Black',
			            fontsize='small'
					)
			plt.tight_layout()
			plt.show()
			return
	else:
		if len(a_data) > 30: # if length larger than 30, create graph with scroll
			graph_w_scroll(a_data, a_per, title, x_label, "Percentage of As")
			return
		else:
			y_lable = "Percentage of As"
			# Create one graph with a size of 10,6
			fig, ax = plt.subplots(figsize=(10,6), num=title + " | " + y_lable + f" | Figure {fig_num}")
			# set graph parameters
			ax.bar(a_data, a_per)
			ax.set_xlabel(x_label)
			ax.set_ylabel(y_lable)
			ax.set_title(title)
			ax.tick_params(axis='x', labelsize=10, rotation=90)
			fig_num += 1
			# add height to the bars
			rect = ax.patches
			for rect, a_per in zip(rect, a_per):
				height = rect.get_height()
				if height >= 4: # Add white text if the height is >= 4
					ax.text(
			            rect.get_x() + rect.get_width() / 2,
			            height - 0.01,
			            round(float(a_per),1),
			            horizontalalignment='center',
			            verticalalignment='top',
			            color='White',
			            fontsize='small'
					)
				else: # else, set the text color to black
					ax.text(
			            rect.get_x() + rect.get_width() / 2,
			            height + 0.01,
			            round(float(a_per),1),
			            horizontalalignment='center',
			            verticalalignment='bottom',
			            color='Black',
			            fontsize='small'
					)
			plt.tight_layout()
			plt.show()
			return

def graph_w_scroll(x, y, title, x_label, y_lable):
	"""
	Summary: 
		- Graphs data using matplotlib with a scroll bar
	Input:
		- x (list) : data for x-axis on the graph
		- y (list) : data for y-axis on the graph
		- title (str) : title of the graph
		- x_label (str) : label for the x-axis
		- y_lable (str) : label for the y-axis
	Return: 
		- a matplotlib graph using plt.show()
	"""
	# Resources: 
		# https://www.geeksforgeeks.org/python-scroll-through-plots/
	# Setting fig and ax variables as subplots()
	global fig_num
	fig, ax = plt.subplots(figsize=(10,6), num=title + " | " + y_lable + f" | Figure {fig_num}")
	ax.tick_params(axis='x', labelsize=10, rotation=90)
	ax.set_xlabel(x_label)
	ax.set_ylabel(y_lable)
	ax.set_title(title)
	plt.tight_layout()
	fig_num += 1
     
    # Adjust the bottom size according to the
	plt.subplots_adjust(bottom=0.25)

    # plot the x and y using bar function
	plt.bar(x, y)
    # Set the axis and slider position in the plot
	axis_position = plt.axes([0.2, 0.0, 0.65, 0.03])
	slider_position = Slider(
			axis_position, # The Axes to put the slider in
			'Pos', # label
			-1, # min value for slider
			len(y)-10, # max value for slider
			valinit=-1.0
		)
	slider_position.valtext.set_visible(False)
    # add height to the bars
	rect = ax.patches
	# https://www.programiz.com/python-programming/methods/built-in/zip
	for rect, y in zip(rect, y):
		height = rect.get_height()
		if height >= 4:
			ax.text(
	            rect.get_x() + rect.get_width() / 2,
	            height - 0.1,
	            round(float(y),1),
	            horizontalalignment='center',
	            verticalalignment='top',
	            color='White',
	            fontsize='small'
			)
		else:
			ax.text(
	            rect.get_x() + rect.get_width() / 2,
	            height + 0.1,
	            round(float(y),1),
	            horizontalalignment='center',
	            verticalalignment='bottom',
	            color='Black',
	            fontsize='small'
			)
	def update(val):
		# Called when slider updates
		# Set the position to where the slider is
		pos = slider_position.val
		# Change the axis information with the new position
		ax.axis([pos, pos+10, 0, 100])
		# redraw the canvas
		fig.canvas.draw_idle()
    # update function called using on_changed() function
	slider_position.on_changed(update)
	# update graph to start at the first element in graph
	update(-1)
    # Display the plot
	plt.show()
	return

# ------------------------------------------------------------------
#						AUXILIARY FUNCTIONS
# ------------------------------------------------------------------
def average_dict(myDict):
	"""
	Summary: 
		- Takes in dictionary with format: {key: [aperc, fperc, total_classes]})
		  and averages the aperc and fperc
	Input:
		- myDict (dict): format {key: [aperc, fperc, total_classes]})
	Return:
		- Averaged aperc and fperc based on total_classes
	"""
	# loop through all elements in myDict
	for i in myDict:
		# 2nd index of dict value is the total number of classes
		# going to use this to average the 1st and 2nd indexes of the dict values
		total_classes = myDict[i][2]
		# Average 'a' score
		if myDict[i][0] != 0 or myDict[i][2] != 0:
			myDict[i][0] = myDict[i][0] / total_classes
		# Average 'd/f' score
		if myDict[i][1] != 0 or myDict[i][2] != 0:
			myDict[i][1] = myDict[i][1] / total_classes
	return myDict


def sort_dict_by_value(d, key_func, reverse=True):
	"""
	Summary: 
		- Sorts dictionary values in order
	Input:
		- d (dict) : Dictionary you want sorted. format {key: [aperc, fperc, total_classes]})
		- key_func (lambda func) : lambda function of item in list you want sorted
		- reverse (bool) : (optional) Sort list by increasing/decreasing order, 
			default sorts in decreasing order
	Return:
		- sorted dictionary
	"""
	# call sort() on dictionary items with lambda function
	return dict(sorted(d.items(), key=lambda item: key_func(item[1]), reverse=reverse))
