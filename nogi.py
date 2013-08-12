import consts


from expression import *
from util import *
from consts import *
from graphs import *


def gen_nogi_table(last, baseops, variables,x):
	# in ops there shouldnot be fold and tfold
	# you must separate them first
	ops=[op for op in baseops if get_arity(op)==1]
	assert "fold" not in ops
	assert "tdold" not in ops
	print 'Generating all nogi of size', last, ", variables: ", es_to_string(variables)

	base = [Const(1)] + variables
	collision_hash={}
	for g in base:
		#yvec=[g.getx(x) for x in xvec]
		y=g.getx(x)
		collision_hash[y]=1
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
			for prev in trees[remain]:
				tree_append(cur,Op1(op,prev),collision_hash,xvec)

		trees[c] = cur
		check_len(len(cur), limit)
		print 'Found ', len(trees[c]), 'programs of size ', c
	return (trees,collision_hash)


def tree_append(cur,el,collision_hash,x):
	#yvec=[el.getx(x) for x in xvec]
	#t=tuple(yvec)
	t=el.getx(x)
	if not collision_hash.has_key(t):
		collision_hash[t]=1
		cur.append(el)

def tree_append2(cur,el,collision_hash,x):
	t=el.getx(x)
	if not collision_hash.has_key(t):
		collision_hash[t]=1
		cur.append(el)
	#yvec=[el.getx(x) for x in xvec]
	#t=tuple(yvec)
	#if not collision_hash.has_key(t):
		# collision_hash[tuple(yvec)]=1
		# cur.append(el)


def gen_tree_table_based_on_legs(last, baseops, variables, xvec, trees, collision_hash):
	# in ops there shouldnot be fold and tfold
	# you must separate them first
	ops=[op for op in baseops if op not in ["shr1","shl1","shr4","shr16"]]
	assert "fold" not in ops
	assert "tdold" not in ops
	print 'Generating all progs of size', last, ", variables: ", es_to_string(variables)


	#assert last <= get_MAX_SIZE(), str(last) + ' is too big'
	limit = get_MAX_GRAPHS()
	print 'bound = ', limit

	for c in xrange(2, last + 1):
		cur = []
		count=0
		if len(trees)<=c:
			trees.append([])
		cur=trees[c]
		for op in ops:
			ar = get_arity(op)
			remain = c - 1
			if ar == 1:
				for prev in trees[remain]:
					count+=1
					tree_append2(cur,Op1(op,prev),collision_hash,xvec)
			if ar == 2:
				for c1 in xrange(1, remain):
					c2 = remain - c1
					assert c2 > 0
					if c1 > c2: break
					if c1 != c2:
						for e1 in trees[c1]:
							for e2 in trees[c2]:
								e = Op2(op, e1, e2)
								if True or check_if_needed(e):
									count+=1
									tree_append2(cur,e,collision_hash,xvec)
									#cur.append(e)
					else:
						for i_e1 in xrange(len(trees[c1])):
							e1 = trees[c1][i_e1]
							for i_e2 in xrange(0, i_e1 + 1):
								e2 = trees[c1][i_e2]
								e = Op2(op, e1, e2)
								if True or check_if_needed(e):
									count+=1
									tree_append2(cur,e,collision_hash,xvec)
									#cur.append(e)

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
									if True or check_if_needed(e):
										count+=1
										tree_append2(cur,e,collision_hash,xvec)
										#cur.append(e)
						check_len(len(cur), limit)

		trees[c] = cur
		check_len(len(cur), limit)
		print 'Found ', len(trees[c]), 'programs of size ', c, 'check', count ,'graphs'
	return trees


const_cache = {}



if __name__=="__main__":
  ops=["shl1","shr1","shr4","shr16","not","and","or","xor","plus","if0"]
  #ops=["shl1","shr4","and","or","xor","plus","if0"]
  # ops=["shl1","shr1","shr4","shr16","not"]
  # ops=["shl1","shr1","shr4","not"]
  

  xvec=[random.randint(0,LAST) for i in xrange(1)]
  xvec=0x55555555
  (nogi,collision_hash)= gen_nogi_table(10,ops,[Var()],xvec)
  tree = gen_tree_table_based_on_legs(15,ops,[Var()],xvec,nogi,collision_hash)
