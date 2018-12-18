#!/usr/bin/python

f = open("input04.txt")
text = [s.rstrip() for s in f.readlines()]
f.close()

#sorting data by date
log = []
for line in text:
	temp = line.split('] ')
	temp[0] = temp[0][1:]
	log.append(temp)
log.sort(key = lambda x : x[0])


current_guard = ""

track = dict()
minute_fall = -1
minute_wake = -1

for entry in log:
	date = entry[0]
	description = entry[1].split(' ')
	if description[0] == "Guard":
		current_guard = description[1]
		if current_guard not in track:
			track[current_guard] = [0] * 60
	elif description[0] == "falls" and description[1] == "asleep":
		minute_fall = int(date[-2:])
	elif description[0] == "wakes" and description[1] == "up":
		minute_wake = int(date[-2:])
		for i in range(minute_fall, minute_wake):
			track[current_guard][i] += 1
		
	else:
		print description
		print "NOPE"
		break
#strategy 1
max_sleep = -1
most_slept_minute = -1
sleepiest_guard = ""
for guard, l in track.iteritems():
	s = 0
	for elem in l:
		s += elem
	if s > max_sleep:
		max_sleep = s
		sleepiest_guard = guard
		max_sleep_in_a_minute = -1
		for i in range(60):
			if l[i] > max_sleep_in_a_minute:
				max_sleep_in_a_minute = l[i]
				most_slept_minute = i
print "strategy 1 result =", most_slept_minute * int(sleepiest_guard[1:])

#strategy 2
max_sleep_in_a_minute = -1
most_slept_minute = -1
sleepiest_guard = ""
for guard, l in track.iteritems():
	for i in range(60):
		if l[i] > max_sleep_in_a_minute:
			most_slept_minute = i
			max_sleep_in_a_minute = l[i]
			sleepiest_guard = guard
print "strategy 2 result =", most_slept_minute * int(sleepiest_guard[1:])
