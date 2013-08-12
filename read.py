import json
import pprint

s = open('problems.json').readline()

#print s
data = json.loads(s)

print len(data)


data.sort(key=lambda x: x["size"])

pprint.pprint(data)

