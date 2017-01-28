import re
import itertools

SDC = 0
I = list() # items list
MS = list() # support counts of items
T = list() # list of transactions
I_MIS_count_support = list() # 4D list with (item, MIS, count, support)
sorted_I_MIS_count_support = list()
L = list() # init-pass(M,T)
F = list() # list of frequent item-sets (that is, list of 1-item-set, 2-item-set, ..)
number_of_transactions = 0
number_of_items = 0

# these 3 functions return values form the 4D list
#-------------------------------------------------
def item(i):
	return sorted_I_MIS_count_support[i][0]

def MIS(i):
	return sorted_I_MIS_count_support[i][1]

def count(i):
	return sorted_I_MIS_count_support[i][2]

def support(i):
	return sorted_I_MIS_count_support[i][3]

#-------------------------------------------------

def find_index_in_M(item): 
	for i, sublist in enumerate(sorted_I_MIS_count_support):
		if item in sublist: # Shouldn't it be checked against sublist[0]?
			return i
	return -1

def find_subl_idx_in_list(item, L):
	for index, sublist in enumerate(L):
		if set(item) == set(sublist[0]):
			return index
	return -1

def init_pass(M, T):
	global L
	# find support counts for each item
	for i in range(len(M)):
		for t in T:
			if M[i][0] in t:
				M[i][2] += 1
		M[i][3] = float(M[i][2])/number_of_transactions
	
	# create L
	for i in range(len(M)):
		if not L:
			if MIS(i) <= support(i): #check <= or <
				L.append(item(i))
				thld = MIS(i)
		else:
			if (support(i) >= thld):
				L.append(item(i))

_I = list()
def process(line):
	global number_of_items
	global SDC
	if re.findall('\((.+?)\)', line):
		_I.append([int(x) for x in re.findall('\((.+?)\)', line)])
		I_MIS_count_support.append([int(x) for x in re.findall('\((.+?)\)', line)])
		I_MIS_count_support[number_of_items].append(float(line.split(' ')[-1]))
		I_MIS_count_support[number_of_items].append(0)
		I_MIS_count_support[number_of_items].append(0)
		number_of_items+=1
	elif re.findall('SDC = ', line):
		SDC = float(line.split(' ')[-1])

def read_parameters():
	global I
	global sorted_I_MIS_count_support
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
	global sorted_I_MIS_count_support
	# sort I_MIS_count_support based on MIS
	sorted_I_MIS_count_support = sorted(M,key=lambda x: (x[1]))

def L2_candidate_gen(L, SDC):
	C2 = list()
	for l in L:
		item1_index_in_M = find_index_in_M(l)
		if MIS(item1_index_in_M) <= support(item1_index_in_M):
			l_index = L.index(l)
			L_after_l = L[l_index + 1:]
			for h in L_after_l:
				item2_index_in_M = find_index_in_M(h)
				if MIS(item1_index_in_M) <= support(item2_index_in_M):
					if abs((support(item2_index_in_M)) - (support(item1_index_in_M))) <= SDC:
						c = [l, h]
						C2.append(c)
	return C2

def MScandidate_gen(F, SDC, k_1):
	Ck = list()
	for i in range(len(F)): #f1
		for ip in range(len(F)): #f2
			if (i != ip):
				# compare the k-2 first items of the two subsets
				for k in range(0,k_1-1):
					if (F[i][0][k] != F[ip][0][k]):
						continue
					index_i = find_index_in_M(F[i][0][k_1-1])
					index_ip = find_index_in_M(F[ip][0][k_1-1])
					if (index_i < index_ip):
						if abs((support(index_i)) - (support(index_ip))) <= SDC:
							c = F[i][0][:-1]
							c.append(F[i][0][k_1-1])
							c.append(F[ip][0][k_1-1])
							Ck.append(c)
							# create k-1 subsets of c
							k_1_subsets = list(itertools.combinations(c, k_1))
							for s in k_1_subsets:
								if (c[0] in s) or (MIS(find_index_in_M(c[1])) == MIS(find_index_in_M(c[0]))):
									for f in F:
										if s in f[0]: # Check ??
											Ck.remove(c)
	return Ck

def msa(T, MS, SDC):
	F1 = list()
	sort(MS)
	init_pass(sorted_I_MIS_count_support, T)
	for l in L:
		item_index_in_M = find_index_in_M(l)
		if MIS(item_index_in_M) <= support(item_index_in_M):
			F1.append([l, count(item_index_in_M)]) 
	F.append(F1)
	k = 2
	while len(F) == k-1:
		Fk = list()
		if k == 2:
			C_k = L2_candidate_gen(L, SDC)
		else:
			C_k = MScandidate_gen(F[k-2], SDC, k-1)
		c_list = list()
		for t in T:
			for index, c in enumerate(C_k):
				if set(c).issubset(set(t)):
					index = find_subl_idx_in_list(c, c_list)
					if index == -1:
						c_list.append([c,1]) # Add c with c.count=0 to c_list
					else:
						c_list[index][1] += 1 # c.count++
		for c in C_k:
			index = find_subl_idx_in_list(c, c_list)
			if index != -1: 
				item_index_in_M = find_index_in_M(c[0])
				if MIS(item_index_in_M) <= float(c_list[index][1])/number_of_transactions:
					Fk.append([c, c_list[index][1]])
		if len(Fk) != 0:
			F.append(Fk)
		k+=1

read_transactions()
read_parameters()
msa(T, I_MIS_count_support, SDC)
# MScandidate_gen(C2, SDC, 2)
