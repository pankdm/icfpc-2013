from solver import *
import code

def first_op(gr):
	return gr.dump().split()[0][1:]

def f(n, m1, m2):
	g = get_all_graphs(n, ["not", "and", "or", "xor", "shr1", "shr4", "shr16", "plus", "shl1", "if0"])
	res = {}
	for gr in g:
		n = gr.getx(m1)
		res[n] = res.get(n, 0) + 1
	return sorted(res.values()), len(res), sum(res.values())
	#code.interact(local=locals())
	#a1 = len(g)
	#a2 = len(set(map(lambda x: x.getx(m1), g)))
	#a3 = len(set(map(lambda x: (x.getx(m1), first_op(x)), g)))
	#a4 = len(set(map(lambda x: x.getx(m2), g)))
	#a5 = len(set(map(lambda x: (x.getx(m2), first_op(x)), g)))
	#a6 = len(set(map(lambda x: (x.getx(m1), x.getx(m2)), g)))
	#a7 = len(set(map(lambda x: (x.getx(m1), x.getx(m2), first_op(x)), g)))
	#return a1, (a2, a3), (a4, a5), (a6, a7)

print f(8, 0, 1234234215)
