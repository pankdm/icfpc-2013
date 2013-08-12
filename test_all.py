from solver import *
from graphs import *
from ft_subgraph import *

def test_op1():
	e0 = Op1("not", Const(0))
	assert e0.getx(0) == LAST
	assert e0.getx(1) == LAST

	ex = Op1("not", Var())
	assert ex.getx(0) == LAST
	assert ex.getx(1) == LAST - 1

	ee = Op1("not", ex)
	for i in xrange(10):
		assert ee.getx(i) == i

def test_shl1():
	assert shl1(LAST) == 0xFFFFFFFFFFFFFFFE
	assert shl1(shl1(LAST)) == 0xFFFFFFFFFFFFFFFC

def test_shr():
	# taken from official site
	assert shr1(0xABC) == 0x55E
	assert shr4(0xABC) == 0xAB
	assert shr16(0xABCDE) == 0xA
	assert shr4(LAST) == 0x0FFFFFFFFFFFFFFF

def test_op2():
	assert Op2("plus", Var(), Const(1)).getx(0x100) == 0x101
	assert Op2("or", Var(), Const(0x11)).getx(0x101) == 0x111
	assert Op2("xor", Var(), Const(0x11)).getx(0x101) == 0x110
	assert Op2("and", Var(), Const(0x11)).getx(0x101) == 0x001

def test_if0():
	e = If0(
			Op2("xor", 
				Op2("and", 
					Var(), 
					Const(1)), 
				Const(1)),
			Var(), 
			Op2("plus", 
				Var(), 
				Const(1)))
	assert e.getx(16) == 17
	assert e.getx(11) == 11

def test_fold():
	e = Fold(
			Var(),
			Const(1),
			Op2("xor",
				Var("y"),
				Var("z")))
	assert e.getx(0x123456789abcdef0) == 0x12 ^ 0x34 ^ 0x56 ^ 0x78 ^ 0x9a ^ 0xbc ^ 0xde ^ 0xf0 ^ 1
	assert e.dump() == "(fold x 1 (lambda (y z) (xor y z)))"

# "(lambda (x_20308) (fold (not (xor 1 x_20308)) 0 (lambda (x_20309 x_20310) (and (not x_20310) x_20309))))"
def test_uncommutative_fold():
	e = Fold(
			Op1("not",
				Op2("xor", Const(1), Var())),
			Const(0),
			Op2("and", Op1("not", Var("z")), Var("y")))

	assert e.getx(0xF0) == 0xF1
	assert e.getx(0x17) == 0x16

def test_dump():
	e = Op1("not", Op1("not", Const(0)))
	text = dump_program(e)
	assert text == "(lambda (x) (not (not 0)))"

def test_graphs():
	assert len(get_graphs_with_given_size(3, ["not"])) == 3
	assert len(get_graphs_with_given_size(3, ["and"])) == 0
	assert len(get_graphs_with_given_size(4, ["and"])) == 6

def test_queue():
  queue=[("a",0.1),("b",0.1),("c",0.1),("d",0.1)]
  queue_put(queue,("e",0.05))
  assert(queue[0][0]=="e")
  queue=[("a",0.1),("b",0.2),("c",0.3),("d",0.4)]
  queue_put(queue,("e",0.35))
  assert(queue[3][0]=="e")
  queue_put(queue,("e",0.25))
  queue=[("a",0.1),("b",0.1),("c",0.1),("d",0.1)]
  queue_put(queue,("e",0.25))
  print queue
  assert(queue[4][0]=="e")

def test_graphs_with_fold():
	gs = get_graphs_with_given_size(6, ["fold"])
	# print es_to_string(gs)
	assert len(gs) == 5 * 3 * 3

	# gs = get_all_graphs(7, ["xor", "fold"])
	# print es_to_string(gs)



TESTS = [test_queue,
	test_dump, test_op1, test_shl1, test_shr, test_op2, test_graphs, test_if0, test_fold,
	test_graphs_with_fold,
	test_uncommutative_fold]

def test():
	for t in TESTS:
		print 'Testing', str(t.func_name)
		t()


test()

