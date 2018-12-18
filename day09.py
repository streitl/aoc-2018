#!/usr/bin/python

def counter_clock(n, pos, circle):
		if (n == 0):
			return pos
		else:
			return counter_clock(n-1, circle[pos][1], circle)

def play(nplayers, nmarbles):
	score = dict()
	for i in range(nplayers):
		score[i+1] = 0

	current = 0
	circle = [[0, 0, 0]]
	for j in range(nmarbles):
		i = j + 1
		playing = j % nplayers + 1
		if i % 23 == 0:
			to_remove = counter_clock(7, current, circle)
			score[playing] += i + circle[to_remove][0]
			
			previous = circle[to_remove][1]
			next = circle[to_remove][2]
			
			circle[previous][2] = next
			circle[next][1] = previous
			
			# useless but marks the "dead" nodes
			circle[to_remove][1] = -1
			circle[to_remove][2] = -1
			
			current = next
		else:
			removed = i/23
			index = i - removed
			
			circle.append([i, 0, 0])
			between = circle[current][2]
			
			# inserted element points next to the element between pointed next to
			circle[index][2] = circle[between][2] 
			# element that was pointed next to by between now points back to inserted
			circle[circle[index][2]][1] = index
			# between now points next to inserted
			circle[between][2] = index
			# inserted element points back to between
			circle[index][1] = between
			
			current = index
	max_score = 0
	for k,v in score.iteritems():
		max_score = max(max_score, v)
	return max_score

f = open("input09.txt")
text = f.readlines()[0].rstrip().split(' ')
f.close()

players = int(text[0])
marbles = int(text[6])

print "Part 1:", play(players, marbles)

print "Part 2:", play(players, marbles*100)

