import consts


from expression import *
from util import *
from consts import *

def get_arity(op):
	if op in ["not", "shr1", "shr4", "shr16", "shl1"]: return 1
	elif op in ["and", "or", "plus", "xor"]: return 2
	elif op in ["if0"]: return 3
	else: assert False, "unknown oprerator: " + op


def check_len(l, limit):
	if l > limit:
		print 'too many graphs:', l
		# custom exception
		print 1 / 0


class TreeTableGenerator:
	def __init__(self, ops, variables, cache):
		self.ops = ops
		self.variables = variables
		self.cache = cache

		base = [Const(0), Const(1)] + variables
		self.trees = [None, None]
		self.trees[1] = base

	def calculate_up_to_yield(self, last):
		# print 'Calculating up to ', last

		cache = self.cache
		trees = self.trees

		if len(trees) == 2:
			for t in trees[1]:
				yield t

		limit = get_MAX_GRAPHS()
		# print 'bound = ', limit

		for c in xrange(len(trees), last + 1):
			while c >= len(trees):
				trees.append([])

			cur = trees[c]
			for op in self.ops:
				ar = get_arity(op)
				remain = c - 1
				if ar == 1:
					for prev in trees[remain]:
						e = Op1(op, prev)
						if cache.add_to_list(cur, e, c):
							yield e
				if ar == 2:
					for c1 in xrange(1, remain):
						c2 = remain - c1
						assert c2 > 0
						if c1 > c2: break
						if c1 != c2:
							for e1 in trees[c1]:
								for e2 in trees[c2]:
									e = Op2(op, e1, e2)
									if cache.add_to_list(cur, e, c):
										yield e
						else:
							for i_e1 in xrange(len(trees[c1])):
								e1 = trees[c1][i_e1]
								for i_e2 in xrange(0, i_e1 + 1):
									e2 = trees[c1][i_e2]
									e = Op2(op, e1, e2)
									if cache.add_to_list(cur, e, c):
										yield e

				if ar == 3:
					for c1 in xrange(1, remain):
						for c2 in xrange(1, remain - c1):
							c3 = remain - c1 - c2
							assert c3 > 0
							for e1 in trees[c1]:
								if e1.is_const: continue
								for e2 in trees[c2]:
									for e3 in trees[c3]:
										e = If0(e1, e2, e3)
										if cache.add_to_list(cur, e, c):
											yield e

			print 'Found ', len(trees[c]), 'programs of size ', c, 'variables: ', es_to_string(self.variables)

	def calculate_up_to2(self, last):
		# print 'Calculating up to ', last

		cache = self.cache
		trees = self.trees

		limit = get_MAX_GRAPHS()
		# print 'bound = ', limit

		for c in xrange(len(trees), last + 1):
			while c >= len(trees):
				trees.append([])

			cur = trees[c]
			for op in self.ops:
				ar = get_arity(op)
				remain = c - 1
				if ar == 1:
					for prev in trees[remain]:
						e = Op1(op, prev)
						cache.add_to_list(cur, e, c)
				if ar == 2:
					for c1 in xrange(1, remain):
						c2 = remain - c1
						assert c2 > 0
						if c1 > c2: break
						if c1 != c2:
							for e1 in trees[c1]:
								for e2 in trees[c2]:
									e = Op2(op, e1, e2)
									cache.add_to_list(cur, e, c)
						else:
							for i_e1 in xrange(len(trees[c1])):
								e1 = trees[c1][i_e1]
								for i_e2 in xrange(0, i_e1 + 1):
									e2 = trees[c1][i_e2]
									e = Op2(op, e1, e2)
									cache.add_to_list(cur, e, c)

				if ar == 3:
					for c1 in xrange(1, remain):
						for c2 in xrange(1, remain - c1):
							c3 = remain - c1 - c2
							assert c3 > 0
							for e1 in trees[c1]:
								if e1.is_const: continue
								for e2 in trees[c2]:
									for e3 in trees[c3]:
										e = If0(e1, e2, e3)
										cache.add_to_list(cur, e, c)

			print 'Found ', len(trees[c]), 'programs of size ', c, 'variables: ', es_to_string(self.variables)



class Cache:
	def __init__(self, points):
		self.const_cache = {}
		self.by_value_cache = {}
		self.points = points
		
	def check_if_needed(self, e):
		if not e.is_const: return True
		if e.value in self.const_cache: return False
		self.const_cache[e.value] = e
		return True

	def add_to_list(self, cur, expression, complexity):
		if self.check_if_needed(expression):
			cur.append(expression)
			return True
		return False
		# if len(self.by_value_cache) > 4 * 10**6:
		# 	cur.append(expression)
		# 	return

		# vs = tuple(expression.get(x, y, z) for x, y, z in self.points)
		# if vs not in self.by_value_cache:
		# 	self.by_value_cache[vs] = 1
		# 	cur.append(expression)



class GraphGenerator:
	def __init__(self, ops, points, values):
		# self.const_cache = {}
		self.by_value_cache = Cache(points)
		self.points = points
		self.values = values
		self.ops = ops

	# TODO: make this more fast
	def can_be_answer(self, expression):
		for i in xrange(len(self.points)):
			x = self.points[i]
			value = self.values[i]
			real = expression.getx(x)
			if  real != value:
				# print 'on x'
				# print 'should be', value
				# print 'we have', real
				return False
		print 'Good possibility: ', expression.dump()
		return True

	def find_first_good(self, size):
		ops = self.ops
		ops, extra = split_by_fold(ops)
		if extra == []:
			# don't consider upper lambda
			last = size - 1
			x_gen = TreeTableGenerator(ops, [Var()], self.by_value_cache)

			# TODO: make more incremental
			for c in xrange(2, last + 1):
				x_gen.calculate_up_to(c)
				# print len(trees)
				for t in trees:
					yield t
			print 'Nothing found'

		elif extra == ["tfold"]:
			# don't consider upper lambda
			# and 4 known complexity from tfold
			last = size - 5
			x_gen = TreeTableGenerator(ops, [Var("y"), Var("z")], self.by_value_cache)
			for c in xrange(2, last + 1):
				trees = x_gen.calculate_up_to_yield(c)
				# trees = x_gen.trees[c]
				for t in trees:
					# print 'gened', t
					expression = TFold(t)
					yield expression
					# if self.can_be_answer(expression):
					# 	print 'found of size', c, "(max size = ", last, ")"
					# 	return expression
		else:
			assert extra == ["fold"]

			# we count complexity of fold as 1
			# we subtract complexity of (lamvda x y) immedaitely
			last = size - 2

			# -3 here is optimization
			# we don't need trees of complexity more than it
			x_gen = TreeTableGenerator(ops, [Var()], self.by_value_cache)
			xyz_gen = TreeTableGenerator(ops, [Var(), Var("y"), Var("z")], self.by_value_cache)
			trees_with_one_fold = [None] * (last + 1)
			cache = self.by_value_cache

			# doesn't exist with such complexity
			trees_with_one_fold[0] = []
			trees_with_one_fold[1] = []
			trees_with_one_fold[2] = []
			trees_with_one_fold[3] = []

			limit = get_MAX_GRAPHS()
			print 'bound = ', limit

			print 'last = ', last
			for c in xrange(4, last + 1):
				x_gen.calculate_up_to2(c - 3)
				xyz_gen.calculate_up_to2(c - 3)

				x_trees = x_gen.trees
				xyz_trees = xyz_gen.trees

				# print "with one fold of size", c
				cur = []
				# gen with top fold
				remain = c - 1
				for c1 in xrange(1, remain):
					for c2 in xrange(1, remain - c1):
						c3 = remain - c1 - c2
						assert c3 > 0
						for e1 in x_trees[c1]:
							for e2 in x_trees[c2]:
								for e3 in xyz_trees[c3]:
									e = Fold(e1, e2, e3)
									yield e
									cache.add_to_list(cur, e, c)

				# gen other
				for op in ops:
					ar = get_arity(op)
					if ar == 1:
						for prev in trees_with_one_fold[remain]:
							e = Op1(op, prev)
							yield e
							cache.add_to_list(cur, e, c)
					if ar == 2:
						for c1 in xrange(1, remain):
							c2 = remain - c1
							for e1 in trees_with_one_fold[c1]:
									for e2 in x_trees[c2]:
										e = Op2(op, e1, e2)
										yield e
										# if self.can_be_answer(e):
										# 	print 'found of size', c, "(max size = ", last, ")"
										# 	return e
										cache.add_to_list(cur, e, c)
							# check_len(len(cur), limit)
					if ar == 3:
						for c1 in xrange(1, remain):
							for c2 in xrange(1, remain - c1):
								c3 = remain - c1 - c2
								assert c3 > 0
								# different locations of fold
								for e1 in trees_with_one_fold[c1]:
									for e2 in x_trees[c2]:
										for e3 in x_trees[c3]:
											e = If0(e1, e2, e3)
											yield e
											cache.add_to_list(cur, e, c)


								for e1 in x_trees[c1]:
									if e1.is_const: continue
									for e2 in x_trees[c2]:
										for e3 in trees_with_one_fold[c3]:
											e = If0(e1, e2, e3)
											yield e
											# if self.can_be_answer(e):
											# 	print 'found of size', c, "(max size = ", last, ")"
											# 	return e
											cache.add_to_list(cur, e, c)


									for e2 in trees_with_one_fold[c2]:
										for e3 in x_trees[c3]:
											e = If0(e1, e2, e3)
											yield e
											# if self.can_be_answer(e):
											# 	print 'found of size', c, "(max size = ", last, ")"
											# 	return e
											cache.add_to_list(cur, e, c)

								# check_len(len(cur), limit)
				trees_with_one_fold[c] = cur
				# check_len(len(cur), limit)
				print 'One Fold: Found ', len(trees_with_one_fold[c]), 'programs of size with ', c


