#!/usr/bin/python

def tree(x):
	s = 0
	v = 0
	nchilds = int(x[0])
	nmeta = int(x[1])
	
	pointer = 2
	pointers = [pointer]
	for i in range(nchilds):
		result = tree(x[pointer:])
		pointer += result[0]
		pointers.append(pointer)
		s += result[1]
			
	for i in range(nmeta):
		s += int(x[pointer + i])
	
	if nchilds == 0:
		for i in range(nmeta):
			v += int(x[pointer + i])
	else:
		for i in range(nmeta):
			index = int(x[pointer + i])
			if index <= nchilds:
				kid_start = pointers[index - 1]
				v += tree(x[kid_start:])[2]
	return (pointer + nmeta, s, v)

f = open("input08.txt")
text = f.readlines()[0].rstrip().split(' ')
f.close()

res = tree(text)
print "Part 1 :", res[1]

print "Part 2 :", res[2]
