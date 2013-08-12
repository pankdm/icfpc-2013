

from solver import *
from graphs import *

f = open("stat/result.txt", "wt")

def is_group(d, mode):
	ops = d["operators"]
	if mode == "fold" or mode == "tfold": return mode in ops
	else: return "fold" not in ops and "tfold" not in ops

s = open('problems.json').readline()
data = json.loads(s)
data.sort(key=lambda x: (x["size"], x["id"]))

Config.TRAINING = True

number = -1
for d in data:
	number += 1

	# if "solved" in d: continue
	if not is_group(d, ""): continue
	if d["size"] < 7: continue
	if d["size"] > 10: break
	print
	print number
	print d
	
	try: 
		table = get_all_graphs(d["size"], d["operators"])
		check = collapse_table(table)
		data = "\t".join(map(str, [number, len(check), d["operators"]]))
		f.write(data + "\n")
	except ZeroDivisionError:
		print
		print 'FOUND ERROR:', number

f.close()







