#!/usr/bin/python

class Nanobot:

	def __init__(self, x, y, z, r):
		self.x = x
		self.y = y
		self.z = z
		self.r = r
	
	def distance_to(self, other):
		return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


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
can_reach = dict()

for nano in nanobots:

	for x in range(nano.x - nano.r, nano.x + nano.r + 1):
		y_freedom = nano.r - abs(x - nano.x)
		
		for y in range(nano.y - y_freedom, nano.y + y_freedom + 1):
			z_freedom = nano.r - abs(x - nano.x) - abs(y - nano.y)
			
			for z in range(nano.z - z_freedom, nano.z + z_freedom + 1):
			
				if (x, y, z) in can_reach:
					can_reach[(x, y, z)] += 1
				else:
					can_reach[(x, y, z)] = 1

closest_d = -1
best_point = None
reached_by = 0

for (k, v) in can_reach.iteritems():
	d = abs(k[0]) + abs(k[1]) + abs(k[2])
	if best_point == None or v > reached_by or (v == reached_by and d < closest_d):
		best_point = k
		reached_by = v
		closest_d = d

print "Part 2 :", closest_d, best_point, reached_by

