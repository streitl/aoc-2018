#!/usr/bin/python

def print_state(field, elves, goblins):
	s = ""
	for j in range(len(field)):
		l = ""
		
		u = []
		for i in range(len(field[j])):
			has_unit = False
			for e in elves:
				if (e.x, e.y) == (i, j):
					l += "E"
					has_unit = True
					u.append(e)
			for g in goblins:
				if (g.x, g.y) == (i, j):
					l += "G"
					has_unit = True
					u.append(g)
					
			if not has_unit:
				l += field[j][i]
		
		l += "   "
		for unit in u:
			l += unit.__repr__()[0] + "(" + str(unit.hp) + ") "
		
		l += "\n"
		s += l
	print s




def neighbors((x, y), field):
	l = []
	
	if field[y - 1][x] == ".":
		l.append( (x, y - 1) )
	
	if field[y][x - 1] == ".":
		l.append( (x - 1, y) )
	
	if field[y][x + 1] == ".":
		l.append( (x + 1, y) )
		
	if field[y + 1][x] == ".":
		l.append( (x, y + 1) )
	
	return l





def contains_unit((x,y), units):
	for u in units:
		if u.x == x and u.y == y:
			return True
	return False





def shortest_path((sx, sy), (fx, fy), field, units):

	visited = set( [(sx, sy)] )
	queue = Queue()
	
	queue.push( ((sx, sy), []) )
	
	possible_paths = []
	
	smallest_d = 100000000
	
	while not queue.empty():
		
		( (px, py), path) = queue.pop()
		
		if (px, py) == (fx, fy) and len(path) <= smallest_d:
			smallest_d = len(path)
			possible_paths.append(path)
			
		elif len(path) < smallest_d:
			for (nx, ny) in neighbors((px, py), field):
				if (nx, ny) not in visited and not contains_unit((nx, ny), units):
					visited.add( (nx, ny) )
					queue.push( ((nx, ny), path + [(nx, ny)]) ) 
	
	if len(possible_paths) == 0:
		return []
	else:
		possible_paths.sort( key = lambda path : (len(path[0]), path[0][1], path[0][0]) )
		return possible_paths[0]
		
	





def find_target(unit, enemies, field):
	
	r = neighbors((unit.x, unit.y), field)
	
	to_attack = None
	lowest_hp = -1
	
	for (x, y) in r:
		for enemy in enemies:
		
			if (enemy.x, enemy.y) == (x, y) and (lowest_hp == -1 or enemy.hp < lowest_hp) and enemy.hp > 0:
				to_attack = enemy
				lowest_hp = enemy.hp
	
	return to_attack




def move(unit, enemies, field, remaining_units):
	path = None
	dmin = -1
	for enemy in enemies:
		for (x,y) in neighbors((enemy.x, enemy.y), field):
			p = shortest_path((unit.x, unit.y), (x, y), field, remaining_units)
			d = len(p)
			
			if d != 0 and (dmin == -1 or d < dmin):
				dmin = d
				path = p
				
			elif d == dmin:
				paths = [p, path]
				paths.sort( key = lambda pa : (pa[-1][1], pa[-1][0]) )
				path = paths[0]
	
	if path != None:
		unit.x, unit.y = path[0]
		return True
	return False
		
		


def get_score(elves, goblins, rounds):
	remaining_units = elves + goblins
	hp_left = 0
	for u in remaining_units:
		if u.hp > 0:
			hp_left += u.hp
		
	return hp_left * rounds






def fight1(elves, goblins):
	over = False
	rounds = 0

	while not over:
		
		units = elves + goblins
		units.sort( key = lambda unit : (unit.y, unit.x) )
		
		print "After", rounds, "rounds :"
		print_state(field, elves, goblins)
		
		for unit in units:
		
			if unit.hp <= 0:
				continue
			
			remaining_units = [ u for u in units if u.hp > 0 ]
			
			enemies = []
			if unit.__repr__().split(" ")[0] == "Elf":
				enemies = goblins
			else:
				enemies = elves
				
			if len(enemies) == 0:
				over = True
				break
			
			to_attack = find_target(unit, enemies, field)
			
			if to_attack == None:
			
				has_moved = move(unit, enemies, field, remaining_units)
				if has_moved:
					to_attack = find_target(unit, enemies, field)
				
			
			if to_attack != None:
			
				unit.attack(to_attack)
				
				if to_attack.isdead():
					if to_attack.__repr__().split(" ")[0] == "Elf":
						elves = [elf for elf in elves if to_attack != elf]
					else:
						goblins = [gob for gob in goblins if to_attack != gob]
				
		
		if not over:
			rounds += 1
			
	print "After", rounds, "rounds, the battle has ended :"
	print_state(field, elves, goblins)
	
	return rounds



def init_fighters(field, extra_attack = 0):
	elves = []
	goblins = []

	for y in range(len(field)):
		for x in range(len(field[y])):
		
			if field[y][x] == "E":
				field[y][x] = "."
				elves.append( Elf(x, y, 3 + extra_attack) )
				
			elif field[y][x] == "G":
				field[y][x] = "."
				goblins.append( Goblin(x, y) )
				
	return (elves, goblins)





def part1(field):
	
	(elves, goblins) = init_fighters(field)
	
	rounds = fight1(elves, goblins)

	print "Part 1 :", get_score(elves, goblins, rounds)



def part2(field):
	
	extra_attack = 1
	too_low = True
	
	found = False
	while not found:
		if too_low:
			extra_attack
		(elves, goblins) = init_fighters(field)
		


class Unit:

	def __init__(self, x, y, power = 3):
		self.x = x
		self.y = y
		self.power = power
		self.hp = 200
		
	def __repr__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ") with " + str(self.hp) + " hp!"
	
	def attack(self, other):
		other.hp -= self.power
		
	def isdead(self):
		return self.hp <= 0
	
	def copy(self):
		return Elf
	
	
		


class Goblin(Unit):
	
	def __repr__(self):
		return "Goblin at " + Unit.__repr__(self)


class Elf(Unit):

	def __repr__(self):
		return "Elf at " + Unit.__repr__(self)
		

class Queue:
	def __init__(self):
		self.array = []
	
	def empty(self):
		return len(self.array) == 0
	
	def push(self, elem):
		self.array.append(elem)
	
	def first(self):
		if self.empty():
			return None
		return self.array[0]
	
	def pop(self):
		
		f = self.first()
				
		self.array = self.array[1:]
		return f
	
		

f = open("input15.txt")
#f = open("test10-15.txt")
lines = f.readlines()
f.close()

field = [ [x for x in y.rstrip()] for y in lines ]

part1(field)


