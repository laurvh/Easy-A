'''
1/19/23 --> made an aper funct as proof of
	concept 

1/22 --> changed aper funct, so if same teacher
	taught more than one class, the average
	percent would be used

1/25 --> code pushed to github

1/26 --> added function to sort teacher data


'''

import json
import matplotlib.pyplot as plt
#from EasyA.parser.parser.py import *

f = open('gd.js', 'r')

data = json.load(f)

def aPer(class_name):
	myDict = {}
	#'instructor': [ average_aper, count] 
	# 	eventually will probably want passing / d - f rate as well
	for i in data[class_name]:
		lname = i['instructor'].split(',')[0].strip()
		total_failing = float(i['dprec']) + float(i['fprec'])

		if lname in myDict:
			# we have a teacher who has taught already
			# add to the count of classes taught
			myDict[lname][2] += 1; 
			myDict[lname][0] += float(i['aprec'])
			myDict[lname][1] += total_failing

		else:
			# first time this teacher has shown up (count is 1)
			#myDict[lname] = [float(i['aprec']), total_failing, 1]
			myDict[lname] = [float(i['aprec']), total_failing, 1]

	myDict = average_dict(myDict)
	sorted_a = sort_dict_by_value(myDict, key_func=lambda x: x[0])
	sorted_f = sort_dict_by_value(myDict, key_func=lambda x: x[1])
	print(sorted_a)
	print(sorted_f)

	#create lists, so mathplots is easier		
	a_instrucs = []
	a_per = []
	f_instrucs = []
	f_per = []

	for i in sorted_a:
		#add how many classes this professors done to name
		a_instrucs.append(i + " (" + str(myDict[i][2]) + ")")
		a_per.append(myDict[i][0])
	# instrucs = []
	for j in sorted_f:
		#instrucs.append(i + " (" + str(myDict[i][2]) + ")")
		f_instrucs.append(j + " (" + str(myDict[j][2]) + ")")
		f_per.append(myDict[j][1])
	print(f'f_instrucs {f_instrucs}\nf_per {f_per}')


	#graphing 
	display_d_f = True
	if display_d_f == True:
		ax = plt.subplot(1, 2, 1)
		ax.barh(a_instrucs, a_per)
		ax.set_xlabel("Percentage of A's")
		ax.set_ylabel("Professors' Last Names")
		ax.set_title(class_name)

		ax = plt.subplot(1, 2, 2)
		ax.barh(f_instrucs, f_per)
		ax.set_xlabel("Percentage of D / F")
		ax.set_ylabel("Professors' Last Names")
		ax.set_title(class_name)
		plt.show()
		return
	else:
		fig, ax = plt.subplots()
		ax.barh(a_instrucs, a_per)
		ax.set_ylabel("Percentage of A's")
		ax.set_xlabel("Professors' Last Names")
		ax.set_title(class_name)
		plt.show()
		return

	#print(myDict)


"""
Graphs needed
	. Single Graph (Could be 2 if they want d/f percentages)
		- Single class (MATH 111)
		- Single Department (MATH)
		- All classes in a department (All MATH 100-level)
	. All classes of a particular level
	. All instructors vs regular faculty
		- all instructos are the default
"""
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

def display_single_class(class_name, class_level, display_d_f=False):
	return


def sort_dict_by_value(d, key_func, reverse=True):
	return dict(sorted(d.items(), key=lambda item: key_func(item[1]), reverse=reverse))


aPer("AAD199")
#aPer("AAAP511")
#aPer("AAD199")


#What if bad input?! (not this problem)


f.close()



