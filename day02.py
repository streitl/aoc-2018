#!/usr/bin/python

f = open("input02.txt")
text = [s.rstrip() for s in f.readlines()]
f.close()

# part 1
count_two = 0
count_three = 0

for line in text:
	letter_counts = dict()
	for letter in line:
		if letter in letter_counts:
			letter_counts[letter] += 1
		else:
			letter_counts[letter] = 1
			
	if 2 in letter_counts.itervalues():
		count_two += 1
		
	if 3 in letter_counts.itervalues():
		count_three += 1
		
print "part 1 checksum", count_two * count_three

box_ids = text
for id1 in box_ids:
	for id2 in box_ids[box_ids.index(id1)+1:]:
		diff = 0
		char_diff = ' '
		for i in range(len(id1)):
			if id1[i] != id2[i]:
				char_diff = id1[i]
				diff += 1
		if diff == 1:
			print "part 2", id1.replace(char_diff, "")
			break
