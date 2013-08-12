import json
import pprint

from solver import is_good, get_all_graphs

s = open('problems.json').readline()

#print s
data = json.loads(s)

print len(data)

data.sort(key=lambda x: x["size"])

res = []
for d in data:
	take = is_good(d["operators"])
	if take:
		res.append(d)

print len(res)

for d in res:
	pprint.pprint(d)
	get_all_graphs(d["size"], d["operators"])



