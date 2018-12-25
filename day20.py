#!/usr/bin/python

f = open("input20.txt")
regex = f.read().rstrip()
f.close()


distance_to = dict()

pos = (0, 0)

stack = []

d = 0


for c in regex:

	if c == "(":
		stack.append((pos, d))
	
	elif c == "|":
		(pos, d) = stack[-1]
		
	elif c == ")":
		(pos, d) = stack[-1]
		del stack[-1]
	
	elif c == "N":
		pos = (pos[0], pos[1] + 1)
		d += 1
		
	elif c == "S":
		pos = (pos[0], pos[1] - 1)
		d += 1
		
	elif c == "E":
		pos = (pos[0] + 1, pos[1])
		d += 1
		
	elif c == "W":
		pos = (pos[0] - 1, pos[1])
		d += 1
	
	if pos in distance_to:
		distance_to[pos] = min(distance_to[pos], d)
	else:
		distance_to[pos] = d

farthest_room = (0, 0)
max_dist = -1

for k, v in distance_to.iteritems():
	if max_dist == -1 or max_dist < v:
		farthest_room = k
		max_dist = v
	
print "Part 1 :", max_dist


farthest_than_thousand = 0

for k, v in distance_to.iteritems():
	if v >= 1000:
		farthest_than_thousand += 1
		
print "Part 2 :", farthest_than_thousand

