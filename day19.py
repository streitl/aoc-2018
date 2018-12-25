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



def execute1(instructions, register):
	
	pointer = 0
	while pointer < len(instructions):

		register[pointer_register] = pointer
		
		(opcode, A, B, C) = tuple(instructions[pointer])
		
		apply(opcode, A, B, C, register)
		
		if pointer == 33:
			print register[2]
		
		pointer = register[pointer_register] + 1
	
	
	
def execute2(instructions, register):

	pointer = 0
	while pointer < len(instructions):

		register[pointer_register] = pointer
		
		if pointer == 1:
			r0 = 0
			r2 = register[2]
			
			for r4 in range(1, r2 + 1):
				if r2 % r4 == 0:
					r0 += r4
			
			register[0] = r0
			register[4] = r4
			pointer = 16
			register[pointer_register] = pointer
		
		(opcode, A, B, C) = tuple(instructions[pointer])
		
		apply(opcode, A, B, C, register)
		
		pointer = register[pointer_register] + 1
		



f = open("input19.txt")
lines = f.readlines()
f.close()


pointer_register = int(lines[0].split(" ")[1])
instructions = [x.rstrip().split(" ") for x in lines[1:]]

for instr in instructions:
	for i in range(3):
		instr[1 + i] = int(instr[1 + i])



r1 = [0, 0, 0, 0, 0, 0]
execute2(instructions, r1)
print "Part 1 :", r1[0]


r2 = [1, 0, 0, 0, 0, 0]
execute2(instructions, r2)
print "Part 2 :", r2[0]

