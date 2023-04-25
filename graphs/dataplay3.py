'''
1/19/23 --> made an aper funct as proof of
	concept 

1/22 --> changed aper funct, so if same teacher
	taught more than one class, the average
	percent would be used

1/26 --> started to pull from parser.py

1/28 --> dealing with if ask for whole department 

1/30 --> fixed whole department to graph in one table,
	 added handling faculty vs GEs (instruct_graph),
	 changed A_percent() to percent_grapher()

'''

#import json
import matplotlib.pyplot as plt
import pparser as p 




FACULTY = p.getFaculty() #this is sooo slow :(





def department_graph(class_list, dep, level):
	# {CLASS_NUM: [aperc, d+fperc, NUM_CLASSES]}
	myDict = {}
	for i in class_list:
		class_data = p.parseGradeData(dep, i, None)
		for j in class_data:
			total_failing = float(j['dprec']) + float(j['fprec'])
			aprec = float(j['aprec'])
			if i in myDict:
				myDict[i][0] += aprec # a percentage
				myDict[i][1] += total_failing # d/f percentage
				myDict[i][2] += 1 # number of classes
			else:
			 	myDict[i] = [aprec, total_failing, 1]
	myDict = average_dict(myDict)
	graph_data(myDict, "Classes", f'All {dep} {level}-level', True)



def instructor_graph(class_name, data, display_d_f, allInstrucs):
	myDict = {}
	#'instructor': [ average_aper, count] 
	for i in data:
		lname = i['instructor'].split(',')[0].strip()
		fname = i['instructor'].split(',')[1].strip()	

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
			# check if we want all instructors or just faculty 
			if not allInstrucs and (fname + " " + lname) in FACULTY[''.join([i for i in class_name if not i.isdigit()])]:
				# just Faculty
				myDict[lname] = [aprec, total_failing, 1]
			elif allInstrucs:
				# all instructors
				myDict[lname] = [aprec, total_failing, 1]



	myDict = average_dict(myDict)
	graph_data(myDict, "Instructor", class_name, display_d_f)
	

def graph_data(myDict, y_label: str, title:str, display_d_f: bool):
	sorted_a = sort_dict_by_value(myDict, key_func=lambda x: x[0])
	sorted_f = sort_dict_by_value(myDict, key_func=lambda x: x[1])

	#create lists, so mathplots is easier		
	a_data = []
	a_per = []
	f_data = []
	f_per = []

	for i in sorted_a:
		#add how many classes this professors done to name
		a_data.append(i + " (" + str(myDict[i][2]) + ")")
		a_per.append(myDict[i][0])
	# instrucs = []
	for j in sorted_f:
		#instrucs.append(i + " (" + str(myDict[i][2]) + ")")
		f_data.append(j + " (" + str(myDict[j][2]) + ")")
		f_per.append(myDict[j][1])

	if display_d_f:
		ax = plt.subplot(1, 2, 1)
		ax.barh(a_data, a_per)
		ax.set_xlabel("Percentage of A's")
		ax.set_ylabel("Classes")
		ax.set_title(title)
		ax.tick_params(axis='y', labelsize=6)

		ax = plt.subplot(1, 2, 2)
		ax.barh(f_data, f_per)
		ax.set_xlabel("Percentage of D / F")
		ax.set_ylabel("Classes")
		ax.set_title(title)
		ax.tick_params(axis='y', labelsize=6)
		plt.tight_layout()
		plt.show()
		return
	else:
		fig, ax = plt.subplots()
		ax.barh(a_data, a_per)
		ax.set_xlabel("Percentage of A's")
		ax.set_ylabel("Classes")
		ax.set_title(title)
		ax.tick_params(axis='y', labelsize=6)
		plt.show()
	return



def average_dict(myDict):
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
	return dict(sorted(d.items(), key=lambda item: key_func(item[1]), reverse=reverse))



def percent_grapher(dep: str, level:str , classNum: str, allInstrucs: bool, display_d_f: bool):
		#Takes all the info and deals with all the cases

			########
			## NEED TO ADD DIFFERENTIATION BETWEEN INSTRUCTOR GRAPH AND CLASS GRAPH
			########
			
		## dep = deparment type = string
		## level = 100, 200, 300, 400, 500, 600 type = string
		##		(None, if not used)
		## classN = class number; type = string (None, if not used)
		## allInstrucs = wether or not they want all instuctors
		##		or just faculty; type = boolean 
		##		(True is want all instuctor, False is just faculty)
		## display_d_f = display failing grade
		##		type = bool
		##		(True is display failing and A's, False is displays just As)

		# Parse all classes in department
		if level == None and classNum == None:
			#we only have department name, go through all the classes
			d = p.parseGradeData(dep, None, None)
			dat = []

			for c in d:
				#all instructors in the department
				dat += d[c]
			instructor_graph(dep, dat, display_d_f, allInstrucs)


		# Parse level in department
		elif level != None and classNum == None:
			# we have the level of the department
			allC = p.getClassNumbers(dep)
			d = allC[int(level)]
			#print(d)
			dat = []

			for c in d:
				dat += p.parseGradeData(dep, c, None)
			#plug into grapher
			instructor_graph(dep+level, dat, display_d_f, allInstrucs)


		elif classNum != None:
			# we have department and class number
			#get data
			d = p.parseGradeData(dep, classNum, None)
			#plug into grapher
			instructor_graph(dep+classNum, d, display_d_f, allInstrucs)

percent_grapher("BI", None, None, True, True)




