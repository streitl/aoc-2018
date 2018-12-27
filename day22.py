#!/usr/bin/python

import heapq

def compute_indexes(depth, target, extra):
	res = []
	for y in range(target[1] + 1 + extra[0]):
		line = []
		
		for x in range(target[0] + 1 + extra[1]):
			
			if (x, y) == (0, 0) or (x, y) == target:
				line.append(0)
				
			elif y == 0:
				line.append(16807 * x)
			
			elif x == 0:
				line.append(48271 * y)
			
			else:
				erosion_left = (line[x - 1] + depth) % 20183
				erosion_up = (res[y - 1][x] + depth) % 20183
				
				line.append(erosion_left * erosion_up)
				
		res.append(line)
	return res




def risk_to_target(risk_level, target):
	risk = 0
	for y in range(target[1] + 1):
		for x in range(target[0] + 1):
			risk += risk_level[y][x]
	return risk




def neighbors((px, py), risk_level):
	
	l = []
	
	if px + 1 < len(risk_level[0]):
		l.append( (px + 1, py) )
	
	if py + 1 < len(risk_level):
		l.append( (px, py + 1) )
	
	if px - 1 >= 0:
		l.append( (px - 1, py) )
	
	if py - 1 >= 0:
		l.append( (px, py - 1) )
	
	return l




def shortest_path(target, risk_level):

	visited = dict()
	visited[(0, 0)] = set(["T"])
	
	queue = [ (0, [(0, 0)], "T") ]
	
	# defines which tool can be used in which region
	allowed_tools = [ set(["C", "T"]), set(["C", "N"]), set(["T", "N"]) ]
	
	while queue:
		
		( time, path, tool ) = heapq.heappop(queue)
		
		last = path[-1]
		
		if last == target and tool == "T":
			return time
		
		# Try changing tools
		for t in allowed_tools[ risk_level[last[1]][last[0]] ]:
			if t not in visited[last]:
				if last in visited:
					visited[last].add(tool)
				else:
					visited[last] = set([tool])
				new_tool = t
				new_time = time + 7
				heapq.heappush(queue, (new_time, path, new_tool) )
				
		
		# Try moving to the neighbors
		for (nx, ny) in neighbors(last, risk_level):
			new_time = time + 1
			new_tool = tool
			new_path = path + [(nx, ny)]
			
			if tool in allowed_tools[ risk_level[ny][nx] ]:
				new_time = time + 1
				new_tool = tool
				if (nx, ny) not in visited:
					visited[ (nx, ny) ] = set([tool])
				elif tool in visited[ (nx, ny) ]:
					continue
				else:
					visited[ (nx, ny) ].add(tool)
				heapq.heappush(queue, (new_time, new_path, new_tool) )

	return -1
	




f = open("input22.txt")
lines = f.readlines()
f.close()


# Terrain preparation
depth = int(lines[0].split(":")[1])
target = tuple( [int(x) for x in lines[1].split(":")[1].split(",")] )

extra = (200, 200)

geologic_index = compute_indexes(depth, target, extra)

erosion_level = [ [ (x + depth) % 20183 for x in line ] for line in geologic_index ]

risk_level = [ [ x % 3 for x in line ] for line in erosion_level ]

# Part 1
print "Part 1 :", risk_to_target(risk_level, target)

# Part 2
print "Part 2 :", shortest_path(target, risk_level)

