#!/usr/bin/python

f = open("input22.txt")
lines = f.readlines()
f.close()

depth = int(lines[0].split(":")[1])
target = tuple( [int(x) for x in lines[1].split(":")[1].split(",")] )


geologic_index = []

for y in range(target[1] + 1):
	line = []
	
	for x in range(target[0] + 1):
	
		if (x, y) == (0, 0) or (x, y) == target:
			line.append(0)
			
		elif y == 0:
			line.append(16807 * x)
		
		elif x == 0:
			line.append(48271 * y)
		
		else:
			erosion_left = (line[x - 1] + depth) % 20183
			erosion_up = (geologic_index[y - 1][x] + depth) % 20183
			
			line.append(erosion_left * erosion_up)
			
	geologic_index.append(line)

erosion_level = [ [ (x + depth) % 20183 for x in line ] for line in geologic_index]

risk_level = [ [ x % 3 for x in line ] for line in erosion_level]


risk = 0

for line in risk_level:
	for elem in line:
	
		risk += elem

print "Part 1 :", risk


