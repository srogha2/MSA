import re
import itertools
import sys

SDC = 0
I = list() # items list
T = list() # list of transactions
I_MIS_count_support = list() # 4D list with (item, MIS, count, support)
sorted_I_MIS_count_support = list()
F = list() # list of frequent item-sets (that is, list of 1-item-set, 2-item-set, ..)
cannot_be_together = list()
must_have = list()
number_of_transactions = 0
number_of_items = 0

if len(sys.argv) == 4:
	pf_name = sys.argv[1]
	if_name = sys.argv[2]
	of_name = sys.argv[3]
else:
	pf_name = "parameter-file.txt"
	if_name = "input-data.txt"
	of_name = "output.txt"

out_file  = open(of_name,'w')
sys.stdout = out_file

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
		if (item == sublist[0]):
			return i
	return -1

def find_subl_idx_in_list(item, L):
	for index, sublist in enumerate(L):
		if set(item) == set(sublist[0]):
			return index
	return -1

def init_pass(M, T):
	L = list()
	# find support counts for each item
	for i in range(len(M)):
		for t in T:
			if M[i][0] in t:
				M[i][2] += 1
		M[i][3] = float(M[i][2])/number_of_transactions
	
	# create L
	for i in range(len(M)):
		if not L:
			if MIS(i) <= support(i):
				L.append(item(i))
				first_MIS = MIS(i)
		else:
			if (support(i) >= first_MIS):
				L.append(item(i))
	return L

_I = list()
def process(line):
	global cannot_be_together
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
	elif re.findall('cannot_be_together: ', line):
		after_colon = re.sub('cannot_be_together: ','',line)
		split = re.split(r'[},\n]+', after_colon)
		index = 0
		for i in range(len(split)):
			if split[i]:
				if (split[i][0] == '{') or (split[i][1] == '{'):
					cannot_be_together.append(map(int, re.findall(r'\d+', split[i])))
					index += 1
				else:
					cannot_be_together[index-1].append(int(re.search(r'\d+', split[i]).group()))
	elif re.findall('must-have: ', line):
		after_colon = re.sub('must-have: ','',line)
		split = after_colon.split(' or ')
		for i in range(len(split)):
			if split[i]:
				must_have.append(int(re.search(r'\d+', split[i]).group()))

def read_parameters():
	global I
	# read items and their MISs from the parameter file
	with open (pf_name) as params:
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
	f = open(if_name, 'r')
	for line in f:
		T.append(process_transactions(line))
		number_of_transactions+=1

def sort(M):
	global sorted_I_MIS_count_support
	# sort I_MIS_count_support based on MIS
	sorted_I_MIS_count_support = sorted(M,key=lambda x: (x[1]))

def check_for_cannot_be_togethers(Ck, c):
	for cbt_set in cannot_be_together:
		matched_items = 0 # tracks the number of matches in "cannot_be_together" sets
		for i in range(len(cbt_set)):
			if (cbt_set[i] in c):
				matched_items += 1
		if (matched_items == 2): # if all the elements in one of the "cannot_be_together" sets matches, then remove c
			Ck.remove(c)
			break # no need to check the rest of "cannot_be_together" sets

def prune_based_on_must_haves(Fk):
	pruned_Fk = list()
	for i in range(len(Fk)):
		for must_have_item in must_have:
			if (must_have_item in Fk[i][0]):
				pruned_Fk.append(Fk[i])
				continue
	return pruned_Fk


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
						check_for_cannot_be_togethers(C2, c);
	return C2

def MScandidate_gen(F, SDC, k_1):
	Ck = list()
	for i in range(len(F)): #f1
		for ip in range(len(F)): #f2
			if (i != ip):
				# compare the k-2 first items of the two subsets
				for k in range(0,k_1-1):
					if (F[i][0][k] != F[ip][0][k]):
						break
					index_i = find_index_in_M(F[i][0][k_1-1])
					index_ip = find_index_in_M(F[ip][0][k_1-1])
					if (index_i < index_ip):
						if abs((support(index_i)) - (support(index_ip))) <= SDC:
							c = F[i][0][:-1]
							c.append(F[i][0][k_1-1])
							c.append(F[ip][0][k_1-1])
							Ck.append(c)
							check_for_cannot_be_togethers(Ck, c);
							# create k-1 subsets of c
							k_1_subsets = list(itertools.combinations(c, k_1))
							for s in k_1_subsets:
								if (c[0] in s) or (MIS(find_index_in_M(c[1])) == MIS(find_index_in_M(c[0]))):
									for f in F:
										if s in f[0]:
											Ck.remove(c)
	return Ck

def msa(T, MS, SDC):
	F1 = list()
	L = list()
	sort(MS)
	L = init_pass(sorted_I_MIS_count_support, T)
	total_f1 = 0
	for l in L:
		item_index_in_M = find_index_in_M(l)
		if MIS(item_index_in_M) <= support(item_index_in_M):
			F1.append([l, count(item_index_in_M)])
			if (l in must_have):
				total_f1 += 1
				if (total_f1 == 1):
					# Printing frequent 1-itemsets
					print "Frequent 1-itemsets\n"
				print "\t",count(item_index_in_M),": {",;sys.stdout.softspace=0;print l,;sys.stdout.softspace=0;print "}"
	if (total_f1 != 0):
		print "\n\tTotal number of frequent 1-itemsets = ", total_f1, "\n"
	if F1:
		F.append(F1)
	k = 2
	while len(F) == k-1:
		Fk = list() # List of candidate-attributes (say, CAs) 
		# where each CA is a list of {candidate (say, C), count, tailcount}
		# where C is a list is a list of items
		if k == 2:
			C_k = L2_candidate_gen(L, SDC)
		else:
			C_k = MScandidate_gen(F[k-2], SDC, k-1)
		c_tail_list = list()
		c_list = list()
		for t in T:
			for index, c in enumerate(C_k):
				if set(c).issubset(set(t)):
					index = find_subl_idx_in_list(c, c_list)
					if index == -1:
						c_list.append([c,1]) # Add c with c.count=1 to c_list 
					else:
						c_list[index][1] += 1 # c.count++
				if set(c[1:len(c)]).issubset(set(t)):
					index = find_subl_idx_in_list(c[1:], c_tail_list)
					if index == -1:
						c_tail_list.append([c[1:],1]) # Add c-c[0] with (c-c[0]).count=1 to c_tail_list
					else:
						c_tail_list[index][1] += 1 # (c-c[0]).count++
		for c in C_k:
			index = find_subl_idx_in_list(c, c_list)
			if index != -1: 
				item_index_in_M = find_index_in_M(c[0])
				if MIS(item_index_in_M) <= float(c_list[index][1])/number_of_transactions:
					tail_index = find_subl_idx_in_list(c[1:], c_tail_list)
					Fk.append([c, c_list[index][1], c_tail_list[tail_index][1]])
		if len(Fk) != 0:
			pruned_Fk = prune_based_on_must_haves(Fk)
			# Printing frequent k-itemsets
			if len(pruned_Fk) > 0:
				print "\nFrequent",k,;sys.stdout.softspace=0;print "-itemsets\n"
			for f in pruned_Fk:
				print "\t", f[1], ": {",;sys.stdout.softspace=0;print str(f[0])[1:-1],;sys.stdout.softspace=0;print "}"
				print "Tailcount =", f[2]
			if len(pruned_Fk) > 0:
				print "\n\tTotal number of frequent",k,;sys.stdout.softspace=0;print "-itemsets = ", len(pruned_Fk), "\n"
			if Fk:
				F.append(Fk)
		k+=1

read_transactions()
read_parameters()
msa(T, I_MIS_count_support, SDC)

# Work Left: Finding out tailcount, Adding the constraints, Improve printing format, Print to file,
# Generating test cases & testing, Manual code review
