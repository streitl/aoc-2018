#!/usr/bin/python

def d1(point):
	s = 0
	for coord in point:
		s += abs(coord)
	return s


def d2(pointA, pointB):
	s = 0
	for i in range(4):
		s += abs(pointA[i] - pointB[i])
	return s


f = open("input25.txt")
points = [ tuple([ int(y) for y in x.split(",") ]) for x in f.readlines() ]
f.close()


points.sort(key = lambda x : d1(x))


constellations = set()

for p in points:
	
	belongs = set()
	
	for const in constellations:
		for pc in const:
			if d2(p, pc) <= 3:
				belongs.add(const)
				break
	
	if len(belongs) == 0:
		constellations.add( frozenset([p]) )
	else:
		new_const = frozenset([p])
		for const in belongs:
			constellations.remove(const)
			new_const = new_const.union(const)
		
		constellations.add(new_const)
	

print "Part 1 :", len(constellations)


