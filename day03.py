#!/usr/bin/python

f = open("input03.txt")
text = [s.rstrip() for s in f.readlines()]
f.close()

claims = dict()

for line in text:
	words = line.split(' ')
	left = int(words[2].split(',')[0])
	top = int(words[2].split(',')[1][:-1])
	sx = int(words[3].split('x')[0])
	sy = int(words[3].split('x')[1])
	
	for x in range(sx):
		for y in range(sy):
			key = str(left + x) + "," + str(top + y)
			if key in claims:
				claims[key] += 1 
			else:
				claims[key] = 1
				
# part 1
counter = 0
for k, v in claims.iteritems():
	if (v != 1):
		counter += 1
print counter

# part 2
for line in text:
	words = line.split(' ')
	id = words[0]
	left = int(words[2].split(',')[0])
	top = int(words[2].split(',')[1][:-1])
	sx = int(words[3].split('x')[0])
	sy = int(words[3].split('x')[1])
	
	overlaps = False
	for x in range(sx):
		for y in range(sy):
			key = str(left + x) + "," + str(top + y)
			if claims[key] != 1:
				overlaps = True
				
	if not overlaps:
		print id

