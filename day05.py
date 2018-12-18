#!/usr/bin/python
def react(s):
	i = 0
	while i < len(s):
		if i == len(s) - 1:
			break
		u1 = s[i]
		u2 = s[i+1]
		if u1.upper() == u2.upper() and u1.islower() == u2.isupper():
			del s[i+1]
			del s[i]
			i = max(i - 1, 0)
		else:
			i += 1
	return s

f = open("input05.txt")
polymer = [s for s in f.readlines()[0].rstrip()]
f.close()

# part 1
reacted = react(polymer[:])
print "Part 1 :", len(reacted)

# part 2
m = dict()
unit_types = "abcdefghijklmnopqrtuvwxyz"

for letter in unit_types:
	fictional = [s for s in polymer if s.lower() != letter]
	m[letter] = len(react(fictional))
	
	
best_letter = ""
smallest = len(reacted)
for k, v in m.iteritems():
	if v < smallest:
		smallest = v
		best_letter = k
print "Part 2 :", best_letter, smallest
