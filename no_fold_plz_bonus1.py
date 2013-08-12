import psyco
psyco.full()

import code
import consts


from expression import *
from util import *
from consts import *

from graphs import get_arity
from random import *
from time import localtime, strftime

from proxy import Proxy
proxy = Proxy()

def op1_getx(op, x):
	if op == "not": v = not64(x)
	elif op == "shr1": v = shr1(x)
	elif op == "shr4": v = shr4(x)
	elif op == "shr16": v = shr16(x)
	elif op == "shl1": v = shl1(x)
	else: assert False, "unknown operator: " + op
	return v

def op2_getxy(op, x, y):
	if op == "and": v = x & y
	elif op == "or": v = x | y
	elif op == "xor": v = x ^ y
	elif op == "plus": v = plus(x, y)
	else: assert False, "unknown operator: " + op
	return v

# Returns array: n-th value = set(possible values of all graphs of size n)
def gen_tree_values(last, ops, keys, right_answer = ()):
	if last > 10:
		last = 10

	result = [None] * (last + 1)
	result[1] = set([((0,)*len(keys), 0), ((1,)*len(keys), 0), (tuple(keys), 0)])

	for i in xrange(2, last + 1):
		st = set()
		for op in ops:
			ar = get_arity(op)
			remain = i - 1
			if ar == 1:
				for (prev_value, flag) in result[remain]:
					if (flag == 1) and (op != "not"):
						continue
					new_value = tuple(map(lambda x: op1_getx(op, x), prev_value))
					if flag == 0:
						st.add((new_value, 0))
					st.add((new_value, 1))
			elif ar == 2:
				for c1 in xrange(1, remain):
					c2 = remain - c1
					#assert c2 > 0
					if c1 > c2: break
					for (prev_value1, flag1) in result[c1]:
						for (prev_value2, flag2) in result[c2]:
							new_value = tuple(map(lambda x, y: op2_getxy(op, x, y), prev_value1, prev_value2))
							st.add((new_value, 1))
			elif ar == 3:
				for c1 in xrange(1, remain):
					for c2 in xrange(1, remain - c1):
						c3 = remain - c1 - c2
						#assert c3 > 0
						for (prev_value1, flag1) in result[c1]:
							for (prev_value2, flag2) in result[c2]:
								for (prev_value3, flag3) in result[c3]:
									new_value = tuple(map(lambda x, y, z: if0(x, y, z), prev_value1, prev_value2, prev_value3))
									st.add((new_value, 1))
			print op,
		print
		result[i] = st
		if right_answer != ():
			if ((right_answer, 0) in st) or ((right_answer, 1) in st):
				return result[:i+1]
		print "%d step is done, size = %d" % (i, len(st))

	return result

def find_all_trees_with_values(trees_values, keys, true_values, ops):

	def recur(level, values_flag):
		values, flag_v = values_flag
		#assert values in trees_values[level]
		if level == 1:
			if values == (0,) * len(values):
				yield Const(0)
			if values == (1,) * len(values):
				yield Const(1)
			if values == tuple(keys):
				yield Var()
			return
		remain = level - 1
		for op in ops:
			ar = get_arity(op)
			if ar == 1:
				for (prev_value, flag) in trees_values[remain]:
					if flag > flag_v:
						continue
					if (flag == 1) and (op != "not"):
						continue
					if tuple(map(lambda x: op1_getx(op, x), prev_value)) == values:
						for prev_tree in recur(remain, (prev_value, flag)):
							#assert tuple(map(lambda x: Op1(op, prev_tree).getx(x), keys)) == values
							yield Op1(op, prev_tree)
			elif ar == 2:
				if flag_v == 0:
					continue
				for c1 in xrange(1, remain):
					c2 = remain - c1
					#assert c2 > 0
					if c1 > c2: break
					for (prev_value1, flag1) in trees_values[c1]:
						for (prev_value2, flag2) in trees_values[c2]:
							if tuple(map(lambda x, y: op2_getxy(op, x, y), prev_value1, prev_value2)) == values:
								for prev_tree1 in recur(c1, (prev_value1, flag1)):
									for prev_tree2 in recur(c2, (prev_value2, flag2)):
										#assert tuple(map(lambda x: Op2(op, prev_tree1, prev_tree2).getx(x), keys)) == values
										yield Op2(op, prev_tree1, prev_tree2)
			elif ar == 3:
				if flag_v == 0:
					continue
				for c1 in xrange(1, remain):
					for c2 in xrange(1, remain - c1):
						c3 = remain - c1 - c2
						#assert c3 > 0
						for (prev_value1, flag1) in trees_values[c1]:
							for (prev_value2, flag2) in trees_values[c2]:
								for (prev_value3, flag3) in trees_values[c3]:
									if tuple(map(lambda x, y, z: if0(x, y, z), prev_value1, prev_value2, prev_value3)) == values:
										for prev_tree1 in recur(c1, (prev_value1, flag1)):
											for prev_tree2 in recur(c2, (prev_value2, flag2)):
												for prev_tree3 in recur(c3, (prev_value3, flag3)):
													#assert tuple(map(lambda x: If0(prev_tree1, prev_tree2, prev_tree3).getx(x), keys)) == values
													yield If0(prev_tree1, prev_tree2, prev_tree3)

	for i in xrange(1, len(trees_values)):
		if ((true_values, 0) in trees_values[i]):
			print "Trying %d-th step" % i, "flag = 0"
			for a in recur(i, (true_values, 0)):
				yield a
		if ((true_values, 1) in trees_values[i]):
			print "Trying %d-th step" % i, "flag = 1"
			for a in recur(i, (true_values, 0)):
				yield a

def f(x):
	if (x >> 20) == 0:
		q = 1
	else:
		q = x | 1
	return (x + (x & q)) & LAST

def find_first_good2(trees_gen, xs, ys):
	print 'Filtering trees'
	delta = 0
	for c in trees_gen:
		delta += 1
		if delta % 1000 == 0:
			print ".",
		good = True
		for j in xrange(len(xs)):
			value = c.getx(xs[j])
			expected = ys[j]
			if value != expected:
				good = False
				break
		if good:
			print 'Skipped', delta
			return c, delta	
	print 'Error: Nothing found'

def solve2(p):
	if "solved" in p: 
		print 'Already solved!'
		return

	ops = p["operators"]
	if ("fold" in ops) or ("tfold" in ops):
		print "solving only without fold"
		return

	if "bonus" not in ops:
		print "Only for bonus"
		return
	ops.remove("bonus")

	AR = tuple([randint(0, LAST) for i in xrange(10)]) + (0, 1, LAST)
	g = gen_tree_values(p["size"], ops, AR)

	hex_input = map(to_hex, AR)

	print "First request at", strftime("%Y-%m-%d %H:%M:%S", localtime())
	data = proxy.make_eval(p["id"], hex_input)
	right_answers = tuple(map(from_hex, data["outputs"]))

	print "right_answers =", right_answers

	h_gen = find_all_trees_with_values(g, AR, right_answers, ops)
	index = 0
	xs, ys = [], []
	h_current = h_gen.next()
	for i in xrange(1000):
		print
		print 'Iterating', i

		# if i < 10:
		# 	ans = [Const(0)] + ans

		solution = dump_program(h_current)
		print 'solution = ', solution
		data = proxy.make_guess(p["id"], solution)
		status = data["status"]
		if status == "win":
			print
			print 'GOT IT!!!   after ', index, 'skips'
			if Config.TRAINING == False:
				fff = open("output\\%s.txt" % str(p["number"]), "wt")
				print >>fff, h_current.dump()
				fff.close()
			break

		if status == "error":
			print 'Error!, proceeding to another guess'
			h_gen.next()

		if status == "mismatch":
			x, y, my = map(from_hex, data["values"])
			xs.append(x)
			ys.append(y)
			h_current, delta = find_first_good2(h_gen, xs, ys)
			index += delta

if __name__ == "__main__":
	seed(0)
	Config.TRAINING = True
	p = proxy.make_train(42)
	solve2(p)
	
	exit()

	OPS = ["not", "and", "or", "xor", "shr1", "shr4", "shr16", "plus", "shl1", "if0"]
	OPS = ["and","if0","or","plus","shr16","shr4"]
	AR = tuple([randint(0, LAST) for i in xrange(1)])

	g = gen_tree_values(12, OPS, AR, tuple(map(f, AR)))
	print len(g[-1]), tuple(map(f, AR)) in g[-1]
	h = find_all_trees_with_values(g, AR, tuple(map(f, AR)), OPS)
	for a in h:
		print a.dump()#, map(lambda x: a.getx(x), AR)
	print len(h)
