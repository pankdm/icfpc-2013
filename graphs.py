import consts


from expression import *
from util import *
from consts import *

def get_arity(op):
	if op in ["not", "shr1", "shr4", "shr16", "shl1"]: return 1
	elif op in ["and", "or", "plus", "xor"]: return 2
	elif op in ["if0"]: return 3
	else: assert False, "unknown oprerator: " + op

def check_if_needed(e):
	if not e.is_const: return True
	if e.value in const_cache: return False
	const_cache[e.value] = e
	return True

def check_len(l, limit):
	if l > limit:
		print 'too many graphs:', l
		# custom exception
		print 1 / 0


def gen_tree_table(last, ops, variables):
	# in ops there shouldnot be fold and tfold
	# you must separate them first
	assert "fold" not in ops
	assert "tdold" not in ops
	print 'Generating all progs of size', last, ", variables: ", es_to_string(variables)

	base = [Const(0), Const(1)] + variables
	trees = [None] * (last + 1)
	trees[1] = base

	assert last <= get_MAX_SIZE(), str(last) + ' is too big'

	limit = get_MAX_GRAPHS()
	print 'bound = ', limit

	for c in xrange(2, last + 1):
		cur = []
		for op in ops:
			ar = get_arity(op)
			remain = c - 1
			if ar == 1:
				for prev in trees[remain]:
					cur.append(Op1(op, prev))
			if ar == 2:
				for c1 in xrange(1, remain):
					c2 = remain - c1
					assert c2 > 0
					if c1 > c2: break
					if c1 != c2:
						for e1 in trees[c1]:
							for e2 in trees[c2]:
								e = Op2(op, e1, e2)
								if check_if_needed(e):
									cur.append(e)
					else:
						for i_e1 in xrange(len(trees[c1])):
							e1 = trees[c1][i_e1]
							for i_e2 in xrange(0, i_e1 + 1):
								e2 = trees[c1][i_e2]
								e = Op2(op, e1, e2)
								if check_if_needed(e):
									cur.append(e)

					check_len(len(cur), limit)
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
									if check_if_needed(e):
										cur.append(e)
						check_len(len(cur), limit)

		trees[c] = cur
		check_len(len(cur), limit)
		print 'Found ', len(trees[c]), 'programs of size ', c
	return trees

const_cache = {}


def get_graphs_with_given_size(size, ops):
	table = get_all_graphs(size, ops)
	return table[-1]

def get_all_graphs(size, ops):
	ops, extra = split_by_fold(ops)
	if extra == []:
		# don't consider upper lambda
		last = size - 1
		
		trees = gen_tree_table(last, ops, [Var()])
		assert len(trees) == last + 1
		
		return trees
	elif extra == ["tfold"]:
		# don't consider upper lambda
		# and 4 known complexity from tfold
		last = size - 5
		trees = gen_tree_table(last, ops, [Var("y"), Var("z")])
		assert len(trees) == last + 1

		res = [None] * (last + 1)
		index = 0
		for t in trees:
			if not t is None:
				for i in xrange(len(t)):																																																																																																													
					trees[index][i] = TFold(t[i])
			index += 1
		return trees
	else:
		assert extra == ["fold"]

		# we count complexity of fold as 1
		# we subtract complexity of (lamvda x y) immedaitely
		last = size - 2

		# -3 here is optimization
		# we don't need trees of complexity more than it
		x_trees = gen_tree_table(last - 3, ops, [Var()])
		xyz_trees = gen_tree_table(last - 3, ops, [Var(), Var("y"), Var("z")])
		trees_with_one_fold = [None] * (last + 1)

		# doesn't exist with such complexity
		trees_with_one_fold[0] = []
		trees_with_one_fold[1] = []
		trees_with_one_fold[2] = []
		trees_with_one_fold[3] = []

		# TODO: get rid of copy paste
		limit = get_MAX_GRAPHS()
		print 'bound = ', limit

		print 'last = ', last
		for c in xrange(4, last + 1):
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
								cur.append(Fold(e1, e2, e3))
			# gen other
			for op in ops:
				ar = get_arity(op)
				# TODO: get rid of copy paste			
				if ar == 1:
					for prev in trees_with_one_fold[remain]:
						cur.append(Op1(op, prev))
				if ar == 2:
					for c1 in xrange(1, remain):
						c2 = remain - c1
						for e1 in trees_with_one_fold[c1]:
								for e2 in x_trees[c2]:
									e = Op2(op, e1, e2)
									cur.append(e)
						check_len(len(cur), limit)
				if ar == 3:
					for c1 in xrange(1, remain):
						for c2 in xrange(1, remain - c1):
							c3 = remain - c1 - c2
							assert c3 > 0
							# different locations of fold
							for e1 in trees_with_one_fold[c1]:
								for e2 in x_trees[c2]:
									for e3 in x_trees[c3]:
										cur.append(If0(e1, e2, e3))

							for e1 in x_trees[c1]:
								if e1.is_const: continue
								for e2 in x_trees[c2]:
									for e3 in trees_with_one_fold[c3]:
										cur.append(If0(e1, e2, e3))

								for e2 in trees_with_one_fold[c2]:
									for e3 in x_trees[c3]:
										cur.append(If0(e1, e2, e3))

							check_len(len(cur), limit)
			trees_with_one_fold[c] = cur
			check_len(len(cur), limit)
			print 'One Fold: Found ', len(trees_with_one_fold[c]), 'programs of size with ', c

		return trees_with_one_fold


