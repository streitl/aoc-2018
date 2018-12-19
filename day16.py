#!/usr/bin/python
from copy import deepcopy


def apply(opcode, A, B, C, register):

	# Addition
	if opcode == "addr":
		register[C] = register[A] + register[B]
	elif opcode == "addi":
		register[C] = register[A] + B
		
	# Multiplication
	elif opcode == "mulr":
		register[C] = register[A] * register[B]
	elif opcode == "muli":
		register[C] = register[A] * B
	
	# Bitwise AND:
	elif opcode == "banr":
		register[C] = register[A] & register[B]
	elif opcode == "bani":
		register[C] = register[A] & B
		
	# Bitwise OR:
	elif opcode == "borr":
		register[C] = register[A] | register[B]
	elif opcode == "bori":
		register[C] = register[A] | B
	
	# Assignement:
	elif opcode == "setr":
		register[C] = register[A]
	elif opcode == "seti":
		register[C] = A
	
	# Greater-than testing:
	elif opcode == "gtir":
		register[C] = int( A > register[B] )
	elif opcode == "gtri":
		register[C] = int( register[A] > B )
	elif opcode == "gtrr":
		register[C] = int( register[A] > register[B] )
	
	# Equality testing:
	elif opcode == "eqir":
		register[C] = int( A == register[B] )
	elif opcode == "eqri":
		register[C] = int( register[A] == B )
	elif opcode == "eqrr":
		register[C] = int( register[A] == register[B] )
	
	else:
		print "Invalid opcode:", opcode
		


def remove_single_set_element_from_other_sets(code, code_number):
	
	for (k, v) in code.iteritems():
		if k != code_number:
			code[k] = code[k] - code[code_number]
	
						

def solve(code):
	for (k, v) in sorted(code.iteritems(), key=lambda (k,v):(len(v), k)):
		if len(v) != 1:
			for opcode in v:
				if consider_this_opcode_for_k(code, k, opcode):
					return True



def consider_this_opcode_for_k(code, code_number, opcode):

	global solved_code

	possible_code = deepcopy(code)
	
	possible_code[code_number] = set([opcode])
	
	remove_single_set_element_from_other_sets(possible_code, code_number)
	
	passed = set()
	solved = True
	for (k, v) in possible_code.iteritems():
		if len(v) == 0:
			return False
		if len(v) > 1:
			solved = False
		if len(v) == 1:
			if v.issubset(passed):
				return False
			else:
				passed = passed.union(v)
			
	
	if solved:
		solved_code = possible_code
		return True
	else:
		return solve(possible_code)
		


def print_code(code):
	for (k, v) in code.iteritems():
		print k, "->", v


f = open("input16.txt")
(part1, part2) = tuple(f.read().split("\n\n\n\n"))
samples = part1.split("\n\n")
instructions = part2.split("\n")[:-1]
f.close()

opcodes = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori", 
		"setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr"]


# Part 1

code = dict()
amount = 0
for sample in samples:
	
	initial_register = [int(x) for x in sample.split("\n")[0].split("[")[1][:-1].split(",")]
	(opcode_number, A, B, C) = tuple([int(x) for x in sample.split("\n")[1].split(" ")])
	expected_register = [int(x) for x in sample.split("\n")[2].split("[")[1][:-1].split(",")]
	
	
	possibilities = set()
	
	for opcode in opcodes:
		register = initial_register[:]
		apply(opcode, A, B, C, register)
		
		possible = True
		for i in range(4):
			if register[i] != expected_register[i]:
				possible = False

		if possible:
			possibilities.add(opcode)
	
	if len(possibilities) >= 3:
		amount += 1
		
	
	
	if opcode_number in code:
		code[opcode_number] = possibilities & code[opcode_number]
	else:
		code[opcode_number] = possibilities
		

print "Part 1 :", amount


#Part 2

for (k, v) in code.iteritems():
	if len(v) == 1:
		remove_single_set_element_from_other_sets(code, k)

solved_code = dict()

solve(code)

code = solved_code

#print "Code"
for (k, v) in code.iteritems():
	code[k] = list(v)[0]
#	print k, "->", code[k]


register = [0, 0, 0, 0]
for instruction in instructions:
	(opcode_number, A, B, C) = tuple([int(x) for x in instruction.split(" ")])
	apply(code[opcode_number], A, B, C, register)

print "Part 2 :", register[0]
