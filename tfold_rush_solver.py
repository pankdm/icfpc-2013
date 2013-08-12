import consts

import json
import pprint

from sys import argv
first = int(argv[1])

import random

last = first
if len(argv) >= 3:
	last = int(argv[2])

from incremental_solver import inc_solve as solve

s = open('problems.json').readline()

#print s
data = json.loads(s)

print len(data)

data.sort(key=lambda x: (x["size"], x["id"]))

# pprint.pprint(data)

random.seed(80)

for i in xrange(first, last + 1):
	print
	print '=' * 80
	print 'Solving problem ', i
	p = data[i]
	p['number'] = i
	print p
	try: 
		solve(p)
	except ZeroDivisionError:
		print
		print 'FOUND ERROR:', i
