

import json


#print s
s = open('problems.json').readline()
data = json.loads(s)

data.sort(key=lambda x: (x["size"], x["id"]))


for i in xrange(len(data)):
	p = data[i]
	if "solved" not in p and "fold" in p["operators"]:
		print "python tfold_rush_solver.py " + str(i) + " "

