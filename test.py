import random
import sys
import math

out_file  = open(sys.argv[1],'w')
sys.stdout = out_file

num_of_transactions = 500
max_size_of_transaction = 5
data_set_granularity = 10
max_num_of_cannot_be_togethers = 10
max_size_of_cannot_be_togethers = 2
max_num_of_must_haves = 4
MIS_start = 0.1
MIS_end = 0.2
SDC_start = 0.1
SDC_end = 0.3

if len(sys.argv) < 2:
	print "Usage: python test.py <transaction_list_file_name> <parameters_file_name>"

i = 0
rand_list = list()
while i < num_of_transactions:
	print "{",;sys.stdout.softspace=0
	size = random.randint(1,max_size_of_transaction)
	j = 1
	rand_list = random.sample(range(1,20),size)
	rand_list[:] = [k * data_set_granularity for k in rand_list] 
	print str(rand_list)[1:-1],;sys.stdout.softspace=0
	print "}"
	i = i + 1

out_file  = open(sys.argv[2],'w')
sys.stdout = out_file

for i in range(data_set_granularity,201,data_set_granularity):
	print "MIS(",;sys.stdout.softspace=0;print i,;sys.stdout.softspace=0;print ") =", round(random.uniform(MIS_start, MIS_end),2)

print "SDC =", round(random.uniform(SDC_start,SDC_end),2)

print "cannot_be_together: ",;sys.stdout.softspace=0
for i in range(0,random.randint(2,max_num_of_cannot_be_togethers)):
	print "{",;sys.stdout.softspace=0;
	print str(random.sample(rand_list, max_size_of_cannot_be_togethers))[1:-1],;sys.stdout.softspace=0;
	print "}, ",;sys.stdout.softspace=0;
print "{",;sys.stdout.softspace=0; print str(random.sample(rand_list, random.randint(1,3)))[1:-1],;sys.stdout.softspace=0; print "}"

print "must-have: ",;sys.stdout.softspace=0
must_have = " or ".join(map(str,random.sample(rand_list, random.randint(2,max_num_of_must_haves))))
print must_have
