import re

SDC = 0
I = list() # items list
MS = list() # support counts of items
T = list() # list of transactions
I_MIS_count = list() # 3D list with (item, MIS, count)
sorted_I_MIS_count = list()
L = list() # init-pass(M,T)
F = list() # list of frequent item-sets (that is, list of 1-item-set, 2-item-set, ..)
number_of_transactions = 0
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
    #global SDC
	if re.findall('\((.+?)\)', line):
		_I.append([int(x) for x in re.findall('\((.+?)\)', line)])
		I_MIS_count.append([int(x) for x in re.findall('\((.+?)\)', line)])
		I_MIS_count[number_of_items].append(float(line.split(' ')[-1]))
		I_MIS_count[number_of_items].append(0)
		number_of_items+=1
	elif re.findall('SDC = ', line):
            SDC = line.split('SDC = ')[1]

def read_parameters():
	global I
	global sorted_I_MIS_count
	# read items and their MISs from the parameter file
	with open ('parameter-file.txt') as params:
		for line in params:
			process(line)
	I = [item for sublist in _I for item in sublist]

def process_transactions(line):
    t = list()
    line = re.sub('[\{\}]','',line)
    for item in line.split(', '):
        t.append(int(item))
    return t

def read_transactions():
    global T
    global number_of_transactions
    f = open('input-data.txt', 'r')
    for line in f:
        T.append(process_transactions(line))
        number_of_transactions+=1

def sort(M):
	global sorted_I_MIS_count
	# sort I_MIS_count based on MIS
	sorted_I_MIS_count = sorted(M,key=lambda x: (x[1]))

def L2_candidate_gen(L, SDC):
    C2 = list()
    for item1, l in enumerate(L):
        if MIS(item1) <= float(count(item1))/number_of_transactions:
            l_index = L.index(l)
            L_after_l = L[l_index + 1:]
            for item2, h in enumerate(L_after_l):
                if MIS(item1) <= float(count(item2))/number_of_transactions:
                    if abs((float(count(item2))/number_of_transactions) - (float(count(item1))/number_of_transactions)) <= SDC:
                        c = [l, h]
                        C2.append(c)
    return C2

def msa(T, MS, SDC):
    F1 = list()
    sort(MS)
    init_pass(sorted_I_MIS_count, T)
    for item, l in enumerate(L):
       if MIS(item) <= float(count(item))/number_of_transactions:
          F1.append(l) 
    F.append(F1)
    i = 2
    while len(F) >= (i-1):
        if i == 2:
            C2 = L2_candidate_gen(L, SDC)
        i+=1

read_transactions()
read_parameters()
msa(T, I_MIS_count, SDC)
