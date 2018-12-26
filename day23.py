#!/usr/bin/python

from heapq import heapify, heappush, heappop

class Nanobot:

	def __init__(self, x, y, z, r):
		self.x = x
		self.y = y
		self.z = z
		self.r = r
	
	def distance_to(self, other):
		return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)
		
	def range_overlaps_with_cube(self, (x1, y1, z1), (x2, y2, z2)):
		assert x1 <= x2 and y1 <= y2 and z1 <= z2
		
		distance = 0
		
		if self.x < x1:
			distance += x1 - self.x
		elif self.x > x2:
			distance += self.x - x2
		
		if self.y < y1:
			distance += y1 - self.y
		elif self.y > y2:
			distance += self.y - y2
		
		if self.z < z1:
			distance += z1 - self.z
		elif self.z > z2:
			distance += self.z - z2
			
		return distance <= self.r



def add_to_heap(x, y, z):
	
	global heap
	global s
	global nanobots
	
	x2 = x + s - 1
	y2 = y + s - 1
	z2 = z + s - 1
	
	in_range = 0
	for bot in nanobots:
		if bot.range_overlaps_with_cube((x, y, z), (x2, y2, z2)):
			in_range += 1
	
	if in_range > 0:
		distance = min(abs(x), abs(x2)) + min(abs(y), abs(y2)) + min(abs(z), abs(z2))
		heappush(heap, (-in_range, distance, s, x, y, z) )


f = open("input23.txt")
lines = f.readlines()
f.close()

# Creation of data structure
nanobots = set()

for line in lines:
	(x, y, z) = tuple( [int(c) for c in line.split("<")[1].split(">")[0].split(",")] )
	r = int(line.split("r=")[1])
	
	nanobots.add( Nanobot(x, y, z, r) )



# Part 1
strongest = None

for nano in nanobots:

	if strongest == None or nano.r > strongest.r:
		strongest = nano
	
in_range = set()

for nano in nanobots:
	if strongest.distance_to(nano) <= strongest.r:
		in_range.add(nano)

print "Part 1 :", len(in_range)
	


# Part 2

xmin = min(bot.x for bot in nanobots)
xmax = max(bot.x for bot in nanobots)

ymin = min(bot.y for bot in nanobots)
ymax = max(bot.y for bot in nanobots)

zmin = min(bot.z for bot in nanobots)
zmax = max(bot.z for bot in nanobots)


s = 1  # size of the cube, a power of two
while s < max(xmax - xmin, ymax - ymin, zmax - zmin):
	s *= 2


heap = [] 

add_to_heap(xmin, ymin, zmin)

while heap:
	in_range, distance, s, x, y, z = heappop(heap)
	
	if s == 1:
		print "Part 2 :", distance
		break
	
	s = s // 2
	
	add_to_heap(x, y, z)
	add_to_heap(x, y, z+s)
	add_to_heap(x, y+s, z)
	add_to_heap(x, y+s, z+s)
	add_to_heap(x+s, y, z)
	add_to_heap(x+s, y, z+s)
	add_to_heap(x+s, y+s, z)
	add_to_heap(x+s, y+s, z+s)

