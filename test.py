import random
import sys
import math

out_file  = open("input.txt",'w')
sys.stdout = out_file

i = 0
rand_list = list()
while i < 100:
	print "{",;sys.stdout.softspace=0
	size = random.randint(1,15)
	j = 1
	rand_list = random.sample(range(1,20),size)
	rand_list[:] = [k * 10 for k in rand_list] 
	print str(rand_list)[1:-1],;sys.stdout.softspace=0
	print "}"
	i = i + 1

out_file  = open("parameter.txt",'w')
sys.stdout = out_file

for i in range(10,201,10):
	print "MIS(",;sys.stdout.softspace=0;print i,;sys.stdout.softspace=0;print ") =", round(random.uniform(0.1, 0.5),2)

print "SDC =", round(random.uniform(0.1,0.3),2)

print "cannot_be_together: ",;sys.stdout.softspace=0
for i in range(0,random.randint(2,6)):
	print "{",;sys.stdout.softspace=0;
	print str(random.sample(rand_list, random.randint(1,3)))[1:-1],;sys.stdout.softspace=0;
	print "}, ",;sys.stdout.softspace=0;
print "{",;sys.stdout.softspace=0; print str(random.sample(rand_list, random.randint(1,3)))[1:-1],;sys.stdout.softspace=0; print "}"

print "must-have: ",;sys.stdout.softspace=0
must_have = " or ".join(map(str,random.sample(rand_list, random.randint(2,6))))
#print str(random.sample(rand_list, random.randint(1,5)))[1:-1]
print must_have
