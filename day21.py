#!/usr/bin/python

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



def execute(instructions, register):
	passed = []
	
	pointer = 0
	while pointer < len(instructions):
		
		if pointer == 28:
		
			if register[3] in passed:
				print "Part 1 :", passed[0]
				print "Part 2 :", passed[-1]
				return
			else:
				passed.append(register[3])
				
			
		register[pointer_register] = pointer
		
		(opcode, A, B, C) = tuple(instructions[pointer])
		
		apply(opcode, A, B, C, register)
		
		pointer = register[pointer_register] + 1



f = open("input21.txt")
lines = f.readlines()
f.close()


pointer_register = int(lines[0].split(" ")[1])
instructions = [x.rstrip().split(" ") for x in lines[1:]]

for instr in instructions:
	for i in range(3):
		instr[1 + i] = int(instr[1 + i])

r = [0, 0, 0, 0, 0, 0]
execute(instructions, r)
