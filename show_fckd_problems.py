import consts

import json
import pprint

s = open('problems.json').readline()

#print s
data = json.loads(s)

print len(data)

data.sort(key=lambda x: x["size"])

res = []
i = 0
for d in data:
	ops = d["operators"]
	d["number"] = i
	#if not any(x in ["fold"] for x in ops):
	if (d.get("timeLeft", -1) == 0) and (d["solved"] == False):
		res.append(d)
	i += 1

print len(res)
pprint.pprint(res)




