#!/usr/bin/python
def distance((x1, y1), (x2, y2)):
	d1 = 0
	if x1>x2:
		d1 = x1 - x2
	else:
		d1 = x2 - x1
	
	d2 = 0
	if y1>y2:
		d2 = y1 - y2
	else:
		d2 = y2 - y1
	return d1 + d2

def find_closest_coordinate((x,y), coordinates):
	min_distance = -1
	closest_coordinate = (0, 0)
	for coord in coordinates:
		d = distance(coord, (x,y))
		if d < min_distance or min_distance == -1:
			min_distance = d
			closest_coordinate = coord
	for coord in coordinates:
		d = distance(coord, (x,y))
		if d == min_distance and coord != closest_coordinate:
			return (-1, -1)
	return closest_coordinate

f = open("input06.txt")
text = [s.rstrip() for s in f.readlines()]
f.close()


coordinates = [tuple(map(lambda x : int(x), x.split(', '))) for x in text]

amount = len(coordinates)

## PART 1 ##
# Computing maximum coordinates
maxx = 0
maxy = 0
for (x,y) in coordinates:
	if x > maxx:
		maxx = x
	if y > maxy:
		maxy = y

#Computing how many points are closest to each coordinate
closest_to = dict()
for i in range(maxx + 1):
	for j in range(maxy + 1):
		coord = find_closest_coordinate((i, j), coordinates)
		if coord in closest_to:
			closest_to[coord] += 1
		else:
			closest_to[coord] = 1

#Finding out which points have an infinite set of closest points
infinites = set()
for i in range(-1, maxx + 2):
	for j in range(-1, maxy + 2):
		if (i == -1 or i == maxx + 1) != (j == -1 or j == maxy + 1):
			coord = find_closest_coordinate((i, j), coordinates)
			infinites.add(coord)

#Removing them from our map
for coord in infinites:
	del closest_to[coord]

#Finding largest area
largest_area = 0
for k, v in closest_to.iteritems():
	if v > largest_area:
		largest_area = v

print "Part 1 - Largest area:", largest_area


## Part 2 ##
MAX_DISTANCE = 10000
region_size = 0
for i in range(maxx + 1):
	for j in range(maxy + 1):
		total_distance = 0
		for coord in coordinates:
			total_distance += distance(coord, (i,j))
		if total_distance < MAX_DISTANCE:
			region_size += 1

print "Part 2 - Region size:", region_size
