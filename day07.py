#!/usr/bin/python

f = open("input07.txt")
text = [s.rstrip() for s in f.readlines()]
f.close()

#preparing data
dependance = dict()
steps = set()

for line in text:
	step = line.split(' ')[7]
	needs = line.split(' ')[1]
	steps.add(step)
	steps.add(needs)
	if step in dependance:
		dependance[step].add(needs)
	else:
		dependance[step] = set([needs])

steps = list(steps)
steps.sort()

#data ready
finished = []

while len(steps) > len(finished):
	for letter in steps:
		if letter not in dependance and letter not in finished:
			finished.append(letter)
			for k,v in dependance.iteritems():
				v.discard(letter)
			dependance = dict([x for x in dependance.iteritems() if len(x[1]) != 0])
			break

print "Part 1:", "".join(finished)



def find_work():
	for letter in todo:
		if letter not in dependance and letter not in processing:
			processing.add(letter)
			works[i] = letter + str(60 + ord(letter) - 64)
			break

for line in text:
	step = line.split(' ')[7]
	needs = line.split(' ')[1]
	if step in dependance:
		dependance[step].add(needs)
	else:
		dependance[step] = set([needs])

works = ['.'] * 5
todo = steps[:]
finished = []
seconds = 0
processing = set()

while len(finished) < len(steps):
	finished_this_second = set()
	for i, w in enumerate(works):
		if w != '.':
			letter = w[:1]
			time = int(w[1:])
			#The worker just finished his task
			if time == 1:
				works[i] = '.'
				finished_this_second.add(letter)
			#He's still doing his task
			else:
				works[i] = letter + str(time - 1)
				
	for letter in finished_this_second:
		processing.discard(letter)
		finished.append(letter)
		todo.remove(letter)
		for k,v in dependance.iteritems():
			v.discard(letter)
		dependance = dict([x for x in dependance.iteritems() if len(x[1]) != 0])
		
	for i, w in enumerate(works):
		if w == '.':
			find_work()
	
	seconds += 1

print "Part 2:", seconds - 1
