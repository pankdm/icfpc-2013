import consts


import json
import random
import ctypes
import pprint

from token import token

from consts import BASE_URL, LAST

def not64(x):
	return ctypes.c_uint64(~x).value

def shr1(x):
	return x >> 1

def shr4(x):
	return x >> 4

def shr16(x):
	return x >> 16

def shl1(x):
	return ((x << 1) & LAST)

def plus(x, y):
	return (x + y) & LAST

def if0(x, y, z):
  if x==0:
    return y
  else :
    return z


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


def PURE_FUNCTION():
	assert False, "Attempting to call pure function"




class Expression:
	def __init__(self):
		# default
		self.is_const = False

	def get(self, x, y, z): PURE_FUNCTION()
	def dump(self): PURE_FUNCTION()
	def getx(self, x):
		return self.get(x, None, None)

class Const(Expression):
	def __init__(self, const):
		self.inner = const
		self.is_const = True
		self.value = const

	def get(self, x, y, z):
		return self.inner

	def dump(self):
		return str(self.inner)

class Var(Expression):
	def __init__(self, var_name = "x"):
		self.var_name = var_name
		self.is_const = False

	def get(self, x, y, z):
		v = self.var_name
		if v == "x": return x
		if v == "y": return y
		if v == "z": return z
		assert "Bad var name"
	
	def dump(self):
		return self.var_name


class Op1(Expression):
	def __init__(self, op, e):
		self.op = op
		self.inner = e
		self.is_const = e.is_const
		if self.is_const: 
			self.value = op1_getx(op, e.value)

	def get(self, x, y, z):
		if self.is_const: return self.value

		value = self.inner.get(x, y, z)
		op = self.op
		return op1_getx(op, value)


	def dump(self):
		return "(%s %s)" %(self.op, self.inner.dump())

class Op2(Expression):
	def __init__(self, op, e1, e2):
		self.op = op
		self.inner1 = e1
		self.inner2 = e2
		self.is_const = e1.is_const and e2.is_const
		if self.is_const:
			self.value = op2_getxy(op, e1.value, e2.value)

	def get(self, x, y, z):
		if self.is_const: return self.value
		v1 = self.inner1.get(x, y, z)
		v2 = self.inner2.get(x, y, z)
		op = self.op
		return op2_getxy(op, v1, v2)

	def dump(self):
		return "(%s %s %s)" %(self.op, self.inner1.dump(), self.inner2.dump())


class If0(Expression):
	def __init__(self, e1, e2, e3):
		self.inner1 = e1
		self.inner2 = e2
		self.inner3 = e3
		self.is_const = e1.is_const and e2.is_const and e3.is_const
		if self.is_const:
			self.value = if0(e1.value, e2.value, e3.value)

	def get(self, x, y, z):
		if self.is_const: return self.value
		v1 = self.inner1.get(x, y, z)
		v2 = self.inner2.get(x, y, z)
		v3 = self.inner3.get(x, y, z)

		if v1 == 0: return v2
		else: return v3

	def dump(self):
		return "(if0 %s %s %s)" %(self.inner1.dump(), self.inner2.dump(), self.inner3.dump())


# optimization of memory
class TFold(Expression):
	def __init__(self, e):
		self.e = e
		self.is_const = False

	def get(self, x, y, z):
		res = 0
		temp = x
		for i in xrange(8):
			res = self.e.get(x, temp % 256, res)
			temp /= 256
		return res

	def dump(self):
		return "(fold x 0 (lambda (y z) %s))" % (self.e.dump())

class Fold(Expression):
	def __init__(self, e1, e2, e3):
		self.e1 = e1  # input array
		self.e2 = e2  # initial value
		self.e3 = e3  # reduce epression
		self.is_const = False

	def get(self, x, y, z):
		res = self.e2.get(x, y, z)
		temp = self.e1.get(x, y, z)
		for i in xrange(8):
			res = self.e3.get(x, temp % 256, res)
			temp /= 256
		return res
	
	def dump(self):
		return "(fold %s %s (lambda (y z) %s))" % (self.e1.dump(), self.e2.dump(), self.e3.dump())
