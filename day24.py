#!/usr/bin/python

def parse_input(lines):
	global initial_groups
	
	for block in lines.split("\n\n"):
		side = block.split("\n")[0][:-1]
		
		for line in block.split("\n")[1:]:
		
			if len(line) == 0:
				break
		
			units = int(line.split("units")[0])
			hp = int(line.split("with")[1].split("hit")[0])
			
			immunities = line.split("immune to ")
			if len(immunities) == 1:
				immunities = []
			else:
				parenthesis_i = immunities[1].find(")")
				semicolon_i = immunities[1].find(";")
				
				c = ""
				if parenthesis_i != -1 and semicolon_i == -1:
					c = ")"
				elif semicolon_i != -1 and parenthesis_i == -1:
					c = ";"
				
				elif semicolon_i < parenthesis_i:
					c = ";"
				elif parenthesis_i < semicolon_i:
					c = ")"
				else:
					print semicolon_i, parenthesis_i, "<--------------------------"
					c = "WTF"
				
				immunities = immunities[1].split(c)[0].split(", ")
				
			weaknesses = line.split("weak to ")
			if len(weaknesses) == 1:
				weaknesses = []
			else:
				parenthesis_i = weaknesses[1].find(")")
				semicolon_i = weaknesses[1].find(";")
				
				c = ""
				if parenthesis_i != -1 and semicolon_i == -1:
					c = ")"
				elif semicolon_i != -1 and parenthesis_i == -1:
					c = ";"
				
				elif semicolon_i < parenthesis_i:
					c = ";"
				elif parenthesis_i < semicolon_i:
					c = ")"
				else:
					print semicolon_i, parenthesis_i, "<--------------------------"
					c = "WTF"
				
				weaknesses = weaknesses[1].split(c)[0].split(", ")
				
			attk_type = line.split("with an attack that does ")[1].split(" ")[1]
			
			attk_damage = int(line.split("with an attack that does ")[1].split(" ")[0])
			
			initiative = int(line.split("at initiative ")[1])
			
			# print units, hp, immunities, weaknesses, attk_type, attk_damage, initiative
			
			g = Group(side, units, hp, immunities, weaknesses, attk_type, attk_damage, initiative)
			
			initial_groups.append(g)
			









def select(groups):
	global debug
	
	targets = set()
	
	groups.sort(key = lambda x : (x.effective_power(), x.initiative), reverse = True)
	
	if debug:
		print "--------------Planning Phase---------------"
	
	for group in groups:
		
		enemy_groups = [x for x in groups if x.side != group.side]
		
		chosen_enemy = None
		max_damage = 0
		
		availiable_enemies = [g for g in enemy_groups if g not in targets]
		
		for enemy in availiable_enemies:
			
			damage = group.simulate_damage(enemy)
			
			if debug:
				print group, "can do", damage, "damage to", enemy
			
			good = False
			
			if chosen_enemy == None:
				good = True
				
			elif damage > max_damage:
				good = True
				
			elif damage == max_damage:
				if enemy.effective_power() > chosen_enemy.effective_power():
					good = True
					
				elif enemy.effective_power() == chosen_enemy.effective_power():
					if enemy.initiative > chosen_enemy.initiative:
						good = True
			
			if good:
				max_damage = damage
				chosen_enemy = enemy
		
		if chosen_enemy != None and max_damage != 0:
			targets.add(chosen_enemy)
			group.target = chosen_enemy
		else:
			group.target = None
			
			
			
			
			
			
			
			
			
			
			
def attack(groups):
	global debug
	
	groups.sort(key = lambda x : x.initiative, reverse = True)
	
	if debug:
		print "-----------Attacking phase------------"
	
	for group in groups:
		
		if group.target != None and group.units > 0:
			group.attack(group.target)
		elif debug:
			print "Group", group, "could not attack (target =", group.target, ")"
			
			
			
			
			
			
			
			
			
			
			
			
			
			
def battle(groups):
	global debug
	
	prev_state = []
	won = False
	while not won:
		prev_groups = [ x.__copy__() for x in groups ]

		if debug:
			print "New round!"
		
		select(groups)
		attack(groups)
		
		# Removing dead groups
		groups = [ x for x in groups if x.units > 0 ]
		
		sides = set()
		for group in groups:
			sides.add(group.side)
		
		won = len(sides) == 1
		
		
		if len(prev_groups) == len(groups):
			same = True
			for i in range(len(groups)):
				if not prev_groups[i] == groups[i]:
					same = False
					break
			if same:
				return None
		
		if debug:
			print "End of Round"
			print " "
			print groups
	
	if len(groups) == 0:
		return None
	else:
		return groups[0].side
			









def count_units(groups):
	winning_side_units = 0
	for group in groups:
		winning_side_units += group.units
		
	return winning_side_units
			
			
			
			
			
			
			
			
			
			

class Group:

	def __init__(self, side, units, hp, immunities, weaknesses, attk_type, attk_damage, initiative):
		self.side = side
		self.units = units
		self.hp = hp
		self.immunities = immunities
		self.weaknesses = weaknesses
		self.attk_type = attk_type
		self.attk_damage = attk_damage
		self.initiative = initiative
		self.target = None
	
	
	def __repr__(self):
		return self.side + "(" + str(self.units) + " units, " + str(self.effective_power()) + " power, " + str(self.hp) + " hp)"
	
	
	def __copy__(self):
		return Group(self.side, self.units, self.hp, self.immunities, self.weaknesses, self.attk_type, self.attk_damage, self.initiative)
	
	
	def __eq__(self, other):
		if other == None:
			return False
		return self.side == other.side and self.units == other.units and self.hp == other.hp and self.immunities == other.immunities and self.weaknesses == other.weaknesses and self.attk_type == other.attk_type and self.attk_damage == other.attk_damage and self.initiative == other.initiative
	
	
	def __hash__(self):
		return id(self)
	
	
	def boosted_copy(self, boost):
		return Group(self.side, self.units, self.hp, self.immunities, self.weaknesses, self.attk_type, self.attk_damage + boost, self.initiative)
	
	
	def effective_power(self):
		return self.units * self.attk_damage
	
	
	def simulate_damage(self, other):
		
		multiplier = None
		if self.attk_type in other.immunities:
			multiplier = 0
			
		elif self.attk_type in other.weaknesses:
			multiplier = 2
		
		else:
			multiplier = 1
			
		return self.effective_power() * multiplier
		
		
	def attack(self, other):
		
		damage = self.simulate_damage(other)
		
		destroyed_units = min(damage / other.hp, other.units)
		
		other.units -= destroyed_units
		
		#print self, "did", damage, "damage to", other, "killing", destroyed_units, "units"
		
	
	def show(self):
		s = self.side + " group with " + str(self.units) + " units with " + str(self.hp) + " hp each, "
		
		if len(self.immunities) == 0:
			s += "no immunities, "
		else:
			s += "immune to "
			for im in self.immunities:
				s += im + ", "
		
		if len(self.weaknesses) == 0:
			s += "no weaknesses, "
		else:
			s += "weak to "
			for we in self.weaknesses:
				s += we + ", "
		
		s += "dealing " + str(self.attk_damage) + " " + self.attk_type + " damage and having " + str(self.initiative) + " initiative."
		print s
		


debug = False

		
f = open("input24.txt")
lines = f.read()
f.close()

initial_groups = []

# Input parsing
parse_input(lines)


# Part 1
groups = [ g.__copy__() for g in initial_groups]
battle(groups)

print "Part 1 :", count_units(groups)




boost = 40

winner = None
while winner != "Immune System":
	
	new_groups = map(lambda x : x.boosted_copy(boost) if x.side == "Immune System" else x.__copy__(), initial_groups )
	
	winner = battle(new_groups)
	print "When boosted by", boost, ", the winner was", winner
	
	boost += 1

print "Part 2 :", count_units(new_groups)

