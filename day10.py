#!/usr/bin/python


def update_positions(positions, speeds):
	newpos = []
	for ((x,y), (vx,vy)) in zip(positions, speeds):
		newpos.append( (x + vx, y + vy) )
	return newpos

def draw_stars(positions, xmin, xmax, ymin, ymax):
	s = [["-" for aaa in range((xmax-xmin + 1))] for bbb in range(ymax-ymin + 1)]
	
	for (x,y) in positions:
		i = x - xmin
		j = y - ymin
		s[j][i] = "#"
	
	for l in s:
		print "".join(l)

f = open("input10.txt")
text = [s.rstrip() for s in f.readlines()]
f.close()

positions = []
speeds = []

xmax = -1000000
xmin =  1000000
ymax = -1000000
ymin =  1000000

for line in text:
	position = line.split('<')[1].split('>')[0].split(',')
	x = int(position[0])
	y = int(position[1])
	
	xmax = max(xmax, x)
	xmin = min(xmin, x)
	
	ymax = max(ymax, y)
	ymin = min(ymin, y)
	
	speed = line.split('<')[2].split('>')[0].split(',')
	vx = int(speed[0])
	vy = int(speed[1])
	
	positions.append( (x, y) )
	speeds.append( (vx, vy) )
	
smallest = 100000

for second in range(20000):

	positions = update_positions(positions, speeds)
	
	xmax = -1000000
	xmin =  1000000
	ymax = -1000000
	ymin =  1000000
	
	for (x,y) in positions:
		xmax = max(xmax, x)
		xmin = min(xmin, x)
		ymax = max(ymax, y)
		ymin = min(ymin, y)
	
	if smallest > (xmax-xmin) + (ymax-ymin):
		smallest = (xmax-xmin) + (ymax-ymin)
		#print second + 1, xmax, xmin, ymax, ymin 
	
	if second == 10830:
		print "After", second + 1, "seconds:"
		draw_stars(positions, xmin, xmax, ymin, ymax)
	
	


