

import consts

import json
import ctypes
import pprint

from time import localtime, strftime, time
from collections import namedtuple
from random import randint

from token import token
from consts import *
from expression import *
from incremental_graphs import *
from util import *

from proxy import Proxy
proxy = Proxy()

import sys


def get_good_function(size, ops, points, vs):
	gg = GraphGenerator(ops, points, vs)
	return gg.find_first_good(size)


def find_first_good2(trees_gen, xs, ys, stop_time):
	print 'Filtering trees'
	delta = 0
	for c in trees_gen:
		delta += 1
		if delta % 10000 == 0:
			print ".",
			sys.stdout.flush()
			if time() > stop_time + 5:
				print 
				print "Game Over, after", delta
				exit(0)
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

# took some xs as points of hashing
# generates functions until it finds the one that seems to be good
# send it to server and if failed, adds given x to xs and go on
def inc_solve(p):
	if "solved" in p: 
		print 'Already solved!'
		return

	ops = p["operators"]
	# if "tfold" not in ops:
	# 	print "solving only tfold"
	# 	return

	if Config.TRAINING == False:
		if "tfold" not in ops and "fold" not in ops:
			print "solving only with (t)fold"
			return


	# xs = [randint(0, LAST)] + [0, 1, 2]
	# ys = []
	# zs = []
	points = []
	for i in xrange(2):
		points.append(randint(0, LAST))
	for i in xrange(2):
		points.append(randint(0, 255))
	points += [0, LAST]

	print points
	xs = points

	hex_input = map(to_hex, xs)

	print "First request at", strftime("%Y-%m-%d %H:%M:%S", localtime())
	stop_time = time() + 300

	data = proxy.make_eval(p["id"], hex_input)
	values = map(from_hex, data["outputs"])

	gg = GraphGenerator(ops, points, values)
	h_gen = gg.find_first_good(p["size"])

	index = 0
	for i in xrange(1000):
		print
		print 'Iterating', i
		h_current, delta = find_first_good2(h_gen, xs, values, stop_time)
		index += delta
		solution = dump_program(h_current)
		print 'solution = ', solution
		data = proxy.make_guess(p["id"], solution)
		status = data["status"]
		if status == "win":
			print
			print 'GOT IT!!!,     after ', index, 'skips'
			if Config.TRAINING == False:
				fff = open("../output/%s.txt" % str(p["number"]), "wt")
				print >>fff, p
				print >>fff, h_current.dump()
				fff.close()
			break
		else:
			if status == "error":
				print 'Error!, proceeding to another guess'

			if status == "mismatch":
				x, v, my = map(from_hex, data["values"])
				points.insert(0, x)
				values.insert(0, v)
				# res = add_mismatched(x)
				# points = res + points
				# values = [v] * len(res) + values
				print 'Added ', (x, v), 'to points'


def add_mismatched(x):
	res = [(x, randint(0, LAST), randint(0, LAST))]
	tmp = x
	for i in xrange(8):
		point = (x, tmp % 256, 0)
		res.append(point)
		tmp /= 256
	return res


if __name__ == "__main__":
	random.seed(0)
	Config.TRAINING = True
	# p = proxy.make_train(8, ["tfold"])
	# p = proxy.make_train(15, ["tfold"])
	p = proxy.make_train(12, ["tfold"])
	inc_solve(p)








