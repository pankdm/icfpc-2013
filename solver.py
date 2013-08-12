
import consts

import json
import random
import ctypes
import pprint

from token import token

from consts import *
from expression import *
from graphs import *
from util import *
from fingertip import make_rand_input
from time import localtime, strftime

import gc

from proxy import Proxy
proxy = Proxy()

def dump_program_string(text):
	return "(lambda (x) %s)" % text

# returns index
def find_first_good(trees, index, xs, ys):
	print 'Filtering', len(trees), 'trees from index', index 
	for i in xrange(index, len(trees)):
		c = trees[i][1]
		good = True
		for j in xrange(len(xs)):
			value = c.getx(xs[j])
			expected = ys[j]
			if value != expected:
				# print f, 'is bad'
				# print to_hex(value), ' != ', to_hex(expected)
				good = False
				break
		if good:
			print 'Stopped at', i, ', complexity = ', trees[i][0], '(max = ', trees[-1][0], ')'
			return i	
	print 'Error: Nothing found'

def collapse_table(table):
	print 'Collapsing table...'
	res = []
	c = 0
	for t in table:
		if not t is None:
			for elem in t:
				res.append((c, elem))
		c += 1
	print 'Done collapsing'
	return res

def solve(p):
	if "solved" in p: 
		print 'Already solved!'
		return

	ops = p["operators"]
	# if "tfold" not in ops:
	# 	print "solving only tfold"
	# 	return

	if ("fold" not in ops):
		print "solving only fold"
		return

	const_cache = {}
	gc.collect()

	table = get_all_graphs(p["size"], p["operators"])
	check = collapse_table(table)
	print 'Total functions = ', len(check)
	raw_input("continue:?")

	xs = [0, 1, 2, 3, 1000, 2000, 3000, 100000000, 20000000000, LAST, LAST - 1, LAST - 1000]
	
	for i in xrange(10):
		xs.append(make_rand_input())

	for i in xrange(10):
		x = random.randint(0, LAST)
		xs.append(x)

	random.shuffle(xs)

	# x_cnt = 5
	# for i in xrange(x_cnt):
	# 	x = random.randint(0, LAST)
	# 	xs.append(x)
	hex_input = map(to_hex, xs)

	print "First request at", strftime("%Y-%m-%d %H:%M:%S", localtime())
	data = proxy.make_eval(p["id"], hex_input)
	ys = map(from_hex, data["outputs"])

	total = len(check)
	index = find_first_good(check, 0, xs, ys)
	print es_to_string(map(lambda x: x[1], check[index: index + 10]))

	# long_ans = Op2("plus", ans[0], Const(0))
	# solution = dump_program(long_ans)
	for i in xrange(1000):
		print
		print 'Iterating', i

		# if i < 10:
		# 	ans = [Const(0)] + ans

		prog = check[index][1]
		solution = dump_program(prog)
		print 'solution = ', solution
		data = proxy.make_guess(p["id"], solution)
		status = data["status"]
		if status == "win":
			print
			print 'GOT IT!!!'
			if Config.TRAINING == False:
				fff = open("../output/%s.txt" % str(p["number"]), "wt")
				print >>fff, p
				print >>fff, prog.dump()
				fff.close()
			break
			break

		if status == "error":
			print 'Error!, proceeding to another guess'
			index += 1

		if status == "mismatch":
			x, y, my = map(from_hex, data["values"])
			xs.insert(0, x)
			ys.insert(0, y)
			index = find_first_good(check, index, xs, ys)


if __name__ == "__main__":
	random.seed(0)
	Config.TRAINING = True
	# p = proxy.make_train(8, ["tfold"])
	p = proxy.make_train(12, ["fold"])
	# p = proxy.make_train(137)
	#solve(p)

