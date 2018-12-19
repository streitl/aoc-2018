#!/usr/bin/python

def evolve(seconds):
	
	global initial_state
	global spread_patterns
	global pattern_size
	
	state = "." * (pattern_size - 1) + initial_state + "." * (pattern_size - 1)

	zero_index = pattern_size - 1

	second = 1
	while second <= seconds:
		if second % 100000 == 0:
			print second
		new_state = "...."
		zero_index += 2
		
		if state[:pattern_size] in spread_patterns and spread_patterns[state[:pattern_size]] == "#":
			zero_index += 1
		
		for i in range(len(state) - pattern_size):
		
			pattern = state[i: i + pattern_size]
			if pattern in spread_patterns:
				new_state += spread_patterns[pattern]
			else:
				new_state += "."
				
		
		state = new_state + "...."
		
		
		while state[:pattern_size] == pattern_size * ".":
			zero_index -= 1
			state = state[1:]
			 
		while state[-pattern_size:] == pattern_size * ".":
			state = state[:-1]
		
		second += 1
	
	
	result = 0
	for i in range(len(state)):
		if state[i] == "#":
			result += (i - zero_index)
	return result


f = open("input12.txt")
lines = f.readlines()
f.close()


initial_state = lines[0].rstrip().split(": ")[1]

spread_patterns = dict([tuple(x.rstrip().split(" => ")) for x in lines[2:]])

pattern_size = 5

res1 = evolve(20)
print "Part 1:", res1


a = 0
b = 0
linear = False
prev = res1
occurrences = 0

s = 21
while occurrences < 5:
	current = evolve(s)
	if current - prev == a:
		occurrences += 1
		b = current - a * s
	else:
		occurrences = 0
	a = current - prev
	prev = current
	s += 1

print "Formula discovered after "+ str(s) + " seconds : sum(s) = s * " + str(a) + " + " + str(b) + ", for s >= " + str(s)

print "Part 2:", 50000000000 * a + b
