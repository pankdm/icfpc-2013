import consts

import json
import pprint

from solver import get_all_graphs

s = open('problems.json').readline()

data = json.loads(s)

data.sort(key=lambda x: x["size"])

ZERO_BITS = ["not", "and", "or", "xor"]
LEFT_BITS = ["fold", "tfold", "shr1", "shr4", "shr16"]
RIGHT_BITS = ["plus", "shl1"]
ALL_BITS = ["if0"]

cnt_not = 0
cnt_fold = 0
for d in data:
	ops = d["operators"]
	size = d["size"]
	if d.get("timeLeft", -1) == 0:
		continue
	if ("tfold" not in ops) and ("fold" not in ops):
		cnt_not += 1
	else:
		cnt_fold += 1

print "with fold:", cnt_fold, ", w/o fold:", cnt_not
