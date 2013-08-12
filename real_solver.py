import consts

import json
import pprint

from sys import argv
first = int(argv[1])

import gc

last = first
if len(argv) >= 3:
	last = int(argv[2])

from solver import solve

s = open('problems.json').readline()

#print s
data = json.loads(s)

print len(data)

data.sort(key=lambda x: (x["size"], x["id"]))

# pprint.pprint(data)

for i in xrange(first, last + 1):
	print
	print '=' * 80
	print 'Solving problem ', i
	gc.collect()
	p = data[i]
	p['number'] = i
	print p
	try: 
		solve(p)
	except ZeroDivisionError:
		print
		print 'FOUND ERROR:', i
