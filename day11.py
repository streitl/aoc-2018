#!/usr/bin/python

def power_level(x, y):

	global serial_number
	
	rackID = x + 10
	power = rackID * y
	power += serial_number
	power *= rackID
	
	#keep only the hundreds digit
	power = power / 100
	power = power % 10
	
	power -= 5
	return power



def compute_results(x, y):
	global results
	global cells
	
	if results[y][x] != "":
		return results[y][x]
		
	if x == 0 and y == 0:
		results[y][x] = cells[y][x]
	elif x == 0 and y != 0:
		results[y][x] = compute_results(x, y - 1) + cells[y][x]
	elif x != 0 and y == 0:
		results[y][x] = compute_results(x - 1, y) + cells[y][x]
	else:
		results[y][x] = compute_results(x - 1, y) + compute_results(x, y - 1) - compute_results(x - 1, y - 1) + cells[y][x]
	return results[y][x]



def summatory(x, y, window_size):
	global results
	
	w = window_size - 1
	
	if x == 0 and y == 0:
		return results[0][0]
	elif x == 0 and y != 0:
		return results[y + w][x + w] - results[y - 1][x + w]
	elif x != 0 and y == 0:
		return results[y + w][x + w] - results[y + w][x - 1]
	else:
		return results[y + w][x + w] - results[y - 1][x + w] - results[y + w][x - 1] + results[y - 1][x - 1]


#main arguments
f = open("input11.txt")
serial_number = int(f.readlines()[0])
f.close()
grid_size = 300

#creating cells with power
cells = []
for y in range(grid_size):
	row = []
	for x in range(grid_size):
		row.append(power_level(x + 1, y +1))
	cells.append(row)

#computing values of helper matrix results
results = []
for y in range(grid_size):
	row = []
	for x in range(grid_size):
		row.append("")
	results.append(row)

compute_results(grid_size - 1, grid_size - 1)



# trying all sizes
best_size = 0

sx = 0
sy = 0

max_power = - grid_size * grid_size * 9

for window_size in range(1, 301): 
	
	max_power_for_size =  - grid_size * grid_size * 9
	
	s3x = 0
	s3y = 0
	
	for y in range(grid_size - window_size):
		for x in range(grid_size - window_size):
			s = summatory(x, y, window_size)
			if s > max_power_for_size:
				max_power_for_size = s
				s3x = x
				s3y = y
				
	if window_size == 3:
		print "Part 1 :", (s3x + 1, s3y + 1)
	
	if max_power_for_size > max_power:
		sx = s3x
		sy = s3y
		max_power = max_power_for_size
		best_size = window_size

print "Part 2 :", (sx + 1, sy + 1), best_size
