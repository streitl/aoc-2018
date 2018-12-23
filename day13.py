#!/usr/bin/python

class Cart:

	def __init__(self, x, y, direction):
		self.x = x
		self.y = y
		self.direction = direction
		self.turns = 0
	
	def move(self, track):
		global intersect
		
		#decide what is the new direction
		if track[self.y][self.x] == "+":
			new_direction = intersect[self.direction][self.turns % 3]
			self.turns += 1
			
		elif track[self.y][self.x] == "/":
		
			if self.direction == ">":
				new_direction = "^"
			elif self.direction == "v":
				new_direction = "<"
			elif self.direction == "<":
				new_direction = "v"
			elif self.direction == "^":
				new_direction = ">"
				
		elif track[self.y][self.x] == "\\":
		
			if self.direction == ">":
				new_direction = "v"
			elif self.direction == "v":
				new_direction = ">"
			elif self.direction == "<":
				new_direction = "^"
			elif self.direction == "^":
				new_direction = "<"
				
		else:
			new_direction = self.direction
		
		#Go to that direction
		self.direction = new_direction
		
		if self.direction == ">":
			self.x += 1
		elif self.direction == "v":
			self.y += 1
		elif self.direction == "<":
			self.x -= 1
		elif self.direction == "^":
			self.y -= 1
		return (self.x, self.y)
	
	def collides(self, carts):

		for cart in carts:
			if cart != self and (self.x, self.y) == (cart.x, cart.y):
				return True
		return False
				


def print_track_with_carts(track, carts):

	to_print = [ line[:] for line in track[:] ]
	
	for cart in carts:
		to_print[cart.y][cart.x] = cart.direction
	
	print "-----------"
	for line in to_print:
		print "".join(line)
	print "-----------"


#Reads from track map, creates cart list and replaces them with normal track elements

def init_carts(track):
	carts = []
	
	for y in range(len(track)):
		for x in range(len(track[y])):
		
			if track[y][x] == ">" or track[y][x] == "<":
				
				carts.append( Cart(x, y, track[y][x]) )
				track[y][x] = "-"
				
			elif track[y][x] == "v" or track[y][x] == "^":
				
				carts.append( Cart(x, y, track[y][x]) )
				track[y][x] = "|"
	return carts




def part1(track):

	carts = init_carts(track)
	
	while True:

		for cart in carts:
			(x, y) = cart.move(track)
			 
			if cart.collides(carts):
				return "Part 1 : " + str(x) + "," + str(y)
				
		carts.sort(key = lambda c : (c.y, c.x) )




def part2(track):
	
	carts = init_carts(track)
	
	while len(carts) > 1:
		
		collisions = set()

		for cart in carts:
			(x, y) = cart.move(track)
			 
			for cart2 in carts:
				if cart != cart2 and (cart.x, cart.y) == (cart2.x, cart2.y):
					collisions.add(cart)
					collisions.add(cart2)
		
		carts = [cart for cart in carts if cart not in collisions]
			
		carts.sort(key = lambda c : (c.y, c.x) )
		
	return "Part 2 : " + str(carts[0].x) + "," + str(carts[0].y)





f = open("input13.txt")
track1 = [ [x for x in y] for y in f.readlines() ]
f.close()

track2 = [ [x for x in y] for y in track1 ]


intersect = dict()
intersect[">"] = ["^", ">", "v"]
intersect["v"] = [">", "v", "<"]
intersect["<"] = ["v", "<", "^"]
intersect["^"] = ["<", "^", ">"]


print part1(track1)

print part2(track2)

