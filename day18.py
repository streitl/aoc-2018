#!/usr/bin/python

def evolve(field):
	result = []
	
	for y in range(len(field)):
		line =[]
		for x in range(len(field[y])):
			neighbor_trees = 0
			neighbor_lumberyards = 0
			
			
			for j in range(y - 1, y + 2):
				for i in range(x - 1, x + 2):
				
					if (i,j) != (x,y):
						if not i < 0 and not j < 0 and not i >= len(field[y]) and not j >= len(field):
							if field[j][i] == "#":
								neighbor_lumberyards += 1
							elif field[j][i] == "|":
								neighbor_trees += 1
					
			if field[y][x] == ".":
				if neighbor_trees >= 3:
					line.append("|")
				else:
					line.append(".")
					
			elif field[y][x] == "|":
				if neighbor_lumberyards >= 3:
					line.append("#")
				else:
					line.append("|")
					
			elif field[y][x] == "#":
				if neighbor_lumberyards * neighbor_trees > 0:
					line.append("#")
				else:
					line.append(".")
					
		result.append(line)

	return result

def resource_value(field):
	wooded = 0
	lumberyarded = 0

	for line in field:
		for elem in line:
		
			if elem == "#":
				lumberyarded += 1
			elif elem == "|":
				wooded += 1
				
	return wooded * lumberyarded

f = open("input18.txt")
field = [ [x for x in y.rstrip()] for y in f.readlines()]
f.close()


# Part 1
for minute in range(1, 11):
	field = evolve(field)

print "Part 1 :", resource_value(field)


# Part 2
reached = set()

pattern = []

while True:
	field = evolve(field)
	
	res = resource_value(field)
	
	minute += 1
	
	if res in reached:
		if res in pattern:
			break
		else:
			pattern.append(res)
		
	else:
		pattern = []
	
	reached.add(res)

remaining = 1000000000 - minute

print "Part 2 :", pattern[remaining % len(pattern)]
