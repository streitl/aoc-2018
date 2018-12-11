#!/usr/bin/python

input = '''Step B must be finished before step K can begin.
Step F must be finished before step I can begin.
Step T must be finished before step U can begin.
Step R must be finished before step Z can begin.
Step N must be finished before step S can begin.
Step X must be finished before step Y can begin.
Step I must be finished before step Y can begin.
Step K must be finished before step L can begin.
Step U must be finished before step J can begin.
Step G must be finished before step L can begin.
Step W must be finished before step A can begin.
Step H must be finished before step Q can begin.
Step M must be finished before step L can begin.
Step P must be finished before step L can begin.
Step L must be finished before step A can begin.
Step V must be finished before step Y can begin.
Step Q must be finished before step Y can begin.
Step Z must be finished before step J can begin.
Step O must be finished before step D can begin.
Step Y must be finished before step A can begin.
Step J must be finished before step E can begin.
Step A must be finished before step E can begin.
Step C must be finished before step E can begin.
Step D must be finished before step E can begin.
Step S must be finished before step E can begin.
Step B must be finished before step R can begin.
Step U must be finished before step O can begin.
Step X must be finished before step I can begin.
Step C must be finished before step S can begin.
Step O must be finished before step S can begin.
Step J must be finished before step D can begin.
Step O must be finished before step E can begin.
Step Z must be finished before step O can begin.
Step J must be finished before step C can begin.
Step P must be finished before step Y can begin.
Step X must be finished before step S can begin.
Step O must be finished before step Y can begin.
Step J must be finished before step A can begin.
Step H must be finished before step C can begin.
Step P must be finished before step D can begin.
Step Z must be finished before step S can begin.
Step T must be finished before step Z can begin.
Step Y must be finished before step C can begin.
Step X must be finished before step H can begin.
Step R must be finished before step Y can begin.
Step T must be finished before step W can begin.
Step L must be finished before step O can begin.
Step G must be finished before step Z can begin.
Step H must be finished before step P can begin.
Step I must be finished before step U can begin.
Step H must be finished before step V can begin.
Step N must be finished before step Y can begin.
Step Q must be finished before step E can begin.
Step H must be finished before step D can begin.
Step P must be finished before step O can begin.
Step T must be finished before step I can begin.
Step W must be finished before step V can begin.
Step K must be finished before step M can begin.
Step R must be finished before step W can begin.
Step B must be finished before step T can begin.
Step U must be finished before step A can begin.
Step N must be finished before step H can begin.
Step F must be finished before step U can begin.
Step Q must be finished before step O can begin.
Step Y must be finished before step S can begin.
Step V must be finished before step O can begin.
Step W must be finished before step C can begin.
Step Y must be finished before step J can begin.
Step T must be finished before step V can begin.
Step N must be finished before step D can begin.
Step U must be finished before step Q can begin.
Step A must be finished before step C can begin.
Step U must be finished before step M can begin.
Step Q must be finished before step S can begin.
Step P must be finished before step V can begin.
Step B must be finished before step Z can begin.
Step W must be finished before step Q can begin.
Step L must be finished before step S can begin.
Step I must be finished before step P can begin.
Step G must be finished before step P can begin.
Step L must be finished before step C can begin.
Step K must be finished before step A can begin.
Step D must be finished before step S can begin.
Step I must be finished before step H can begin.
Step R must be finished before step M can begin.
Step Q must be finished before step D can begin.
Step K must be finished before step O can begin.
Step I must be finished before step C can begin.
Step N must be finished before step O can begin.
Step R must be finished before step X can begin.
Step P must be finished before step C can begin.
Step B must be finished before step Y can begin.
Step G must be finished before step E can begin.
Step L must be finished before step V can begin.
Step W must be finished before step Y can begin.
Step C must be finished before step D can begin.
Step M must be finished before step J can begin.
Step F must be finished before step N can begin.
Step T must be finished before step Q can begin.
Step I must be finished before step E can begin.
Step A must be finished before step D can begin.'''


#preparing data
dependance = dict()
steps = set()

for line in input.split('\n'):
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

for line in input.split('\n'):
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
	print seconds, works

print "Part 2:", seconds - 1
