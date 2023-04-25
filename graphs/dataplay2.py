'''
1/19/23 --> made an aper funct as proof of
	concept 

1/22 --> changed aper funct, so if same teacher
	taught more than one class, the average
	percent would be used

1/26 --> started to pull from parser.py

1/28 --> dealing with if ask for whole department 



'''

#import json
import matplotlib.pyplot as plt
import pparser as p 



def main(dep: str, level:str , classNum: str, allInstrucs: bool, list_dept_num: bool):
		#Takes all the info and deals with all the cases
			########
			# DOESN'T DEAL WITH ALLiINSTUCS YET
			########

		## dep = deparment type = string
		## level = 100, 200, 300, 400, 500, 600 type = string
		##	(None, if not used)
		## classN = class number; type = string (None, if not used)
		## allInstrucs = wether or not they want all instuctors
		##	or just faculty; type = boolean 
		##	(True is want all instuctor, False is just faculty)

		# Parse all classes in department
		if level == None and classNum == None:
			#we only have department name, go through all the classes
			data = p.parseGradeData(dep, None, None)
			all_class_graph(data, dep)

		# Parse level in department
		elif level != None and classNum == None:
			# we have the level of the department
			allC = p.getClassNumbers(dep)
			data = allC[int(level)]
			if list_dept_num:
				department_graph(data, dep, level)
			else:
				return


		# Parse individual class
		elif classNum != None:
			# we have department and class number
			#get data
			d = p.parseGradeData(dep, classNum, None)
			#plug into aPer
			instructor_graph(dep + classNum, d)

def all_class_graph(class_list, dep):
	"""
	Input:
		- class_list (dict) : dictionary provided from web scraper 
		- dep (str) : Department of class (ie MATH, BI, CS)
	Return: 
		- None
	"""
	myDict = {}
	for i in class_list:
		for j in class_list[i]:
			lname = j['instructor'].split(',')[0]
			total_failing = float(j['dprec']) + float(j['fprec'])
			aprec = float(j['aprec'])
			if lname in myDict:
				myDict[lname][0] += aprec 			# a percentage
				myDict[lname][1] += total_failing 	# d/f percentage
				myDict[lname][2] += 1 				# number of classes
			else:
				myDict[lname] = [aprec, total_failing, 1]
	myDict = average_dict(myDict)
	graph_data(myDict, "Instructor", f'All {dep} Classes', False)

def department_graph(class_list, dep, level):
	"""
	Input:
		- class_list () : 
		- dep (str) : Department of class (ie MATH, BI, CS)
		- level (str) : Level of class (ie 122, 314)
	Return: 
		- None
	"""
	# mydict = {class_num_1: [aperc, d+fperc, number_of_classes], class_num_2: [...]}
	myDict = {}
	# Loop over the list of classes 
	for i in class_list:
		class_data = p.parseGradeData(dep, i, None)
		for j in class_data:
			total_failing = float(j['dprec']) + float(j['fprec'])
			aprec = float(j['aprec'])
			if i in myDict:
				myDict[i][0] += aprec 			# a percentage
				myDict[i][1] += total_failing 	# d/f percentage
				myDict[i][2] += 1 				# number of classes
			else:
			 	myDict[i] = [aprec, total_failing, 1]
	myDict = average_dict(myDict)
	graph_data(myDict, "Classes", f'All {dep} {level}-level', False)

def instructor_graph(class_name, data):
	"""
	Input:
		- class_name (str) : Name of the class
		- data (dict) : Dictionary from the scraper
	Return: 
		- None
	"""
	myDict = {}
	#'instructor': [ average_aper, count] 
	# 	eventually will probably want passing / d - f rate as well
	for i in data:
		lname = i['instructor'].split(',')[0].strip()
		total_failing = float(i['dprec']) + float(i['fprec'])
		aprec = float(i['aprec'])

		if lname in myDict:
			# we have a teacher who has taught already
			# add to the count of classes taught
			myDict[lname][2] += 1; 
			myDict[lname][0] += aprec
			myDict[lname][1] += total_failing

		else:
			# first time this teacher has shown up (count is 1)
			#myDict[lname] = [float(i['aprec']), total_failing, 1]
			myDict[lname] = [aprec, total_failing, 1]

	myDict = average_dict(myDict)
	graph_data(myDict, "Instructor", class_name, True)
	

def graph_data(myDict, y_label: str, title:str, display_d_f: bool):
	sorted_a = sort_dict_by_value(myDict, key_func=lambda x: x[0])
	sorted_f = sort_dict_by_value(myDict, key_func=lambda x: x[1])

	#create lists, so mathplots is easier		
	a_data = []
	a_per = []
	f_data = []
	f_per = []

	#add how many classes this professors done to name
	for i in sorted_a:
		a_data.append(i + " (" + str(myDict[i][2]) + ")")
		a_per.append(myDict[i][0])
	for j in sorted_f:
		f_data.append(j + " (" + str(myDict[j][2]) + ")")
		f_per.append(myDict[j][1])

	if display_d_f:
		# Create 2 graphs and plot
		ax = plt.subplot(1, 2, 1)
		ax.barh(a_data, a_per)
		ax.set_xlabel("Percentage of A's")
		ax.set_ylabel(y_label)
		ax.set_title(title)
		ax.tick_params(axis='y', labelsize=6)

		ax = plt.subplot(1, 2, 2)
		ax.barh(f_data, f_per)
		ax.set_xlabel("Percentage of D / F")
		ax.set_ylabel(y_label)
		ax.set_title(title)
		ax.tick_params(axis='y', labelsize=6)
		plt.tight_layout()
		plt.show()
		return
	else:
		# Create one graph
		fig, ax = plt.subplots()
		ax.barh(a_data, a_per)
		ax.set_xlabel("Percentage of A's")
		ax.set_ylabel(y_label)
		ax.set_title(title)
		ax.tick_params(axis='y', labelsize=6)
		plt.show()
	return

def average_dict(myDict):
	"""
	Input:
		- myDict (dict): format {key: [aperc, fperc, total_classes]})
	Return:
		- Averaged aperc and fperc based on total_classes
	"""
	for i in myDict:
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
	Input:
		- d (dict) : Dictionary you want sorted. format {key: [aperc, fperc, total_classes]})
		- key_func (lambda func) : lambda function of item in list you want sorted
		- reverse (bool) : Sort list by increasing/decreasing order
	Return:
		- sorted dictionary
	"""
	return dict(sorted(d.items(), key=lambda item: key_func(item[1]), reverse=reverse))



main("MATH", None, None, True, False)
#main("MATH", None, "111", True)


#What if bad input?! (not this problem)


#f.close()



