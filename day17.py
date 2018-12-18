#!/usr/bin/python
import sys

sys.setrecursionlimit(2500)

def parse_line(line):
	global xmin, xmax, ymin, ymax
	t = line.split(", ")
	(left, right) = (t[0], t[1])
	
	if left[0] == "x":
		x = int(left.split('=')[1])
		if x > xmax:
			xmax = x
		elif x < xmin:
			xmin = x
		temp = right.split('=')[1].split("..")
		
		yl = int(temp[0])
		yr = int(temp[1])
		
		if yr > ymax:
			ymax = yr
		if yl < ymin:
			ymin = yl
		
		for y in range(yl, yr+1):
			clays.add((x,y))
		
	elif left[0] == "y":
		y = int(left.split('=')[1])
		if y > ymax:
			ymax = y
		if y < ymin:
			ymin = y
			
		temp = right.split('=')[1].split("..")
		
		xl = int(temp[0])
		xr = int(temp[1])
		
		if xr > xmax:
			xmax = xr
		if xl < xmin:
			xmin = xl
			
		for x in range(xl, xr+1):
			clays.add((x,y))
				
	else:
		print "ERROR: expected x or y, found", left[0]
		
		
		

def create_world(clays, xmin, xmax, ymax):
	w = [["." for x in range(xmax-xmin+1)] for y in range(ymax+1)]
	w[0][500-xmin] = "+"
		
	for (x,y) in clays:
		w[y][x-xmin] = "#"
	return w
	
	


def left_right(world, i, j):
	#explore left
	n = i - 1
	c = (n >= 0 and world[j][n] not in collisions)
	leaks = False
	while c:
		if n < 1:
			c = False
			leaks = True
		if c and world[j][n-1] == "#":
			c = False
		if world[j+1][n] not in collisions:
			if world[j+1][n] == "_" or explore(world, n, j + 1):
				leaks = True
				c = False
		n -= 1
	l = n + 1
	
	#explore right
	n = i + 1
	c = (n < len(world[0]) and world[j][n] not in collisions)
	while c:
		if n > len(world[0]) - 2:
			c = False
			leaks = True
		if c and world[j][n+1] == "#":
			c = False
		if world[j+1][n] not in collisions:
			if world[j+1][n] == "_" or explore(world, n, j + 1):
				c = False
				leaks = True
		n += 1
	
	r = n
	if leaks:
		for x in range(l, r):
			world[j][x] = "_"
	else:
		for x in range(l, r):
			world[j][x] = "~"
	return leaks





def explore(world, i, j):

	global collisions
	global ymax
	global xmin
	global xmax
	
	if j > ymax:
		return True
	if i < 0 or i > len(world[0]):
		return True
	
	if j == ymax:
		world[j][i] = "|"
		
		return True
		
	if world[j+1][i] not in collisions:
		if not (j == 0 and i == 500 - xmin):
			world[j][i] = "|"
			
		if world[j+1][i] == "_":
			return True
			
		if not explore(world, i, j + 1):
			world[j][i] = "~"
			return left_right(world, i, j)
		else:
			return True
	else:
		world[j][i] = "~"
		return left_right(world, i, j)


#main

clays = set();

ymin =  10000
ymax = -1
xmin =  10000
xmax = -10000

text = open("input17.txt")

for line in text.readlines():
	parse_line(line)

text.close()

xmin -= 1
xmax += 1

world = create_world(clays, xmin, xmax, ymax)

collisions = set(["#", "~"])

explore(world, 500-xmin, 0)

counter1 = 0
counter2 = 0
for w in world[ymin:]:
	for c in w:
		if c == "~":
			counter1 += 1
			counter2 += 1
		if c == "|" or c == "_":
			counter1 += 1

print "Part 1", counter1
print "Part 2", counter2
