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






def fight1(elves, goblins, field):
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
	new_field = []
	
	for y in range(len(field)):
		line = []
		for x in range(len(field[y])):
		
			if field[y][x] == "E":
				line.append(".")
				elves.append( Elf(x, y, 3 + extra_attack) )
				
			elif field[y][x] == "G":
				line.append(".")
				goblins.append( Goblin(x, y) )
			
			else:
				line.append(field[y][x])
		
		new_field.append(line)
				
	return (new_field, elves, goblins)





def part1(field):
	
	(new_field, elves, goblins) = init_fighters(field)
	
	rounds = fight1(elves, goblins, new_field)

	print "Part 1 :", get_score(elves, goblins, rounds)






def fight2(elves, goblins, field, extra_attack):
	over = False
	rounds = 0

	while not over:
		
		units = elves + goblins
		units.sort( key = lambda unit : (unit.y, unit.x) )
		
		print "After", rounds, "rounds : (Elves are boosted by", extra_attack, ")"
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
						return (False, -1)
					else:
						goblins = [gob for gob in goblins if to_attack != gob]
				
		
		if not over:
			rounds += 1
	
	
	if len(elves) == 0:
		return (False, -1)
	else:
		return (True, rounds)





def part2(field):
	
	'''extra_attack = 21
	
	fails = set()
	works = dict()
	
	diff = 1
	
	found = False
	while not found:
	
		(new_field, elves, goblins) = init_fighters(field, extra_attack)
		
		(elves_won, rounds) = fight2(elves, goblins, new_field, extra_attack)
		
		if elves_won:
			works[extra_attack] = get_score(elves, goblins, rounds)
			
			if extra_attack - 1 in fails:
				print "Part 2 :", works[extra_attack]

				found = True
				
			else:
				diff = max(1, diff // 2)
				extra_attack -= diff
				
		else:
			fails.add(extra_attack)
			
			if extra_attack + 1 in works:
				print "Part 2 :", works[extra_attack + 1]
				found = True
			
			if extra_attack + 2 * diff not in works:
				diff *= 2
			extra_attack += diff'''
	extra_attack = 1
	
	found = False
	while not found:
		(new_field, elves, goblins) = init_fighters(field, extra_attack)
		
		(elves_won, rounds) = fight2(elves, goblins, new_field, extra_attack)
		
		if elves_won:
			print "Part 2 :", get_score(elves, goblins, rounds)
			found = True
		else:
			extra_attack += 1


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

#part1(field)

part2(field)

