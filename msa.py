import re

# SDC = 0
I = list() # items list
MS = list() # support counts of items
I_MIS_count = list() # 3D list with (item, MIS, count)
sorted_I_MIS_count = list()
L = list() # init-pass(M,T)
T = [[20, 80], [10, 20, 80]]
number_of_transactions = 2
number_of_items = 0

# these 3 functions return values form the 3D list
#-------------------------------------------------
def MIS(i):
	return sorted_I_MIS_count[i][1]

def count(i):
	return sorted_I_MIS_count[i][2]

def item(i):
	return sorted_I_MIS_count[i][0]
#-------------------------------------------------

def init_pass(M, T):
	# find support counts for each item
	for i in range(len(M)):
		for t in T:
			if M[i][0] in t:
				M[i][2] += 1
	# create L
	for i in range(len(M)):
		if not L:
			if MIS(i) <= float(count(i))/number_of_transactions:
				L.append(item(i))
				thld = MIS(i)
		else:
			if (float(count(i))/number_of_transactions >= thld):
				L.append(item(i))

_I = list()
def process(line):
	global number_of_items
	if re.findall('\((.+?)\)', line):
		_I.append([int(x) for x in re.findall('\((.+?)\)', line)])
		I_MIS_count.append([int(x) for x in re.findall('\((.+?)\)', line)])
		I_MIS_count[number_of_items].append(float(line.split(' ')[-1]))
		I_MIS_count[number_of_items].append(0)
		number_of_items+=1

def read_parameters():
	global I
	global sorted_I_MIS_count
	# read items and their MISs from the parameter file
	with open ('parameter-file.txt') as params:
		for line in params:
			process(line)
	I = [item for sublist in _I for item in sublist]
	

def sort(M):
	global sorted_I_MIS_count
	# sort I_MIS_count based on MIS
	sorted_I_MIS_count = sorted(M,key=lambda x: (x[1]))

read_parameters()
sort(I_MIS_count)
init_pass(sorted_I_MIS_count, T)





