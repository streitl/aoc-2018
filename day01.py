#!/usr/bin/python


f = open("input01.txt")
text = [s.rstrip() for s in f.readlines()]
f.close()

# part 1
s = 0
for elem in text:
	s += int(elem)
print "part 1", s

# part 2
s = 0
reached = set([0])
repeated = False
while not repeated:
	for elem in text:
		s += int(elem)
		if s not in reached:
			reached.add(s)
		else:
			print "part 2", s
			repeated = True
			break

