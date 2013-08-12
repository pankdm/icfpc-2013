

def to_hex(x):
	# upper case is important
	return "0x%X" % x

def from_hex(x):
	return int(x, 16)


#es is a list of expresssions
def es_to_string(es):
	return "[" + ",".join(map(lambda x: x.dump(), es)) + "]"


# separate (t)fold expressions from ops
def split_by_fold(ops):
	res = []
	extra = []
	for op in ops:
		if op == "fold" or op == "tfold":
			extra.append(op)
		else:
			res.append(op)
	return res, extra

def dump_program(ex):
	text = ex.dump()
	return "(lambda (x) %s)" % text
