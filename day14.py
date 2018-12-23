#!/usr/bin/python

f = open("input14.txt")
wanted_recipes = int(f.read())
f.close()


# Part 1
board = [3, 7]

elf = [0, 1]

created_recipes = 2

while created_recipes < wanted_recipes + 10:
	
	combination = board[elf[0]] + board[elf[1]]
	
	if combination < 10:
		board.append(combination)
		created_recipes += 1
	else:
		first_new_recipe = combination / 10
		second_new_recipe = combination % 10
		board.append(first_new_recipe)
		board.append(second_new_recipe)
		
		created_recipes += 2
	
	elf[0] = (elf[0] + 1 + board[elf[0]]) % len(board)
	elf[1] = (elf[1] + 1 + board[elf[1]]) % len(board)
	
print "Part 1 :", "".join([str(x) for x in board[wanted_recipes:wanted_recipes + 10]])



# Part 2
board = "37"

elf = [0, 1]

created_recipes = 2

wanted_recipes = str(wanted_recipes)

window = ""

recipes_to_the_left = 0

while True:
	
	combination = int(board[elf[0]]) + int(board[elf[1]])
	
	if combination < 10:
		board += str(combination)
		
		created_recipes += 1
		
		window = board[-len(wanted_recipes):]
		if window == wanted_recipes:
			recipes_to_the_left = created_recipes - len(wanted_recipes)
			break
		
	else:
		first_new_recipe = combination / 10
		second_new_recipe = combination % 10
		board += str(first_new_recipe) + str(second_new_recipe)
		
		created_recipes += 2
		
		window = board[-len(wanted_recipes) - 1 : -1]
		if window == wanted_recipes:
			recipes_to_the_left = created_recipes - 1 - len(wanted_recipes)
			break
			
		window = board[-len(wanted_recipes):]
		if window == wanted_recipes:
			recipes_to_the_left = created_recipes - len(wanted_recipes)
			break
	
	elf[0] = (elf[0] + 1 + int(board[elf[0]])) % len(board)
	elf[1] = (elf[1] + 1 + int(board[elf[1]])) % len(board)

print "Part 2 :", recipes_to_the_left
