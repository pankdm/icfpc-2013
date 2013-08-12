from consts import LAST
import random
import expression as e
import copy

random.seed(0)

ops=set(["0","1","x","shl1","shr1","shr4","shr16","not","and","or","xor","plus","if0"])
ops123=set(["shl1","shr1","shr4","shr16","not","and","or","xor","plus","if0"])

nops={"0":0,"1":0,"x":0,"shl1":1,"shr1":1,"shr4":1,"shr16":1,"not":1,"and":2,"or":2,"xor":2,"plus":2,"if0":3,"fold":3}
def schange(x):
  cur=0
  k=0 
  changes=[]
  while x>0 or cur>0:
    if x%2 != cur:
      changes.append(k)
      cur = 1 - cur
    x = x/2
    k +=1
  return changes

def schange2x(changes):
  x=0
  for (k,change) in enumerate(changes):
    x += (2**change-1)*((-1)**(k+1))
  return x



def make_rand_input(N=6,maxi=64):
  ch=[]
  N=2*(N/2)
  for i in range(N):
    ch.append(random.randint(0,maxi))
  ch.sort()
  #return ch
  return schange2x(ch)


def bestshift(chx,chy):
  (maxk,maxd)=(0,0)
  for d in xrange(-64,64):
    (k,ix,iy)=(0,0,0)
    while ix<len(chx) and iy<len(chy):
      #print ix,iy,chx[ix]+d-chy[iy]
      if chx[ix]+d==chy[iy]:
        k +=1
        ix+=1
        iy +=1
      elif chx[ix]+d>chy[iy]:
        iy +=1
      elif chx[ix]+d<chy[iy]:
        ix +=1

    #print d,k
    if k>maxk:
      (maxk,maxd)=(k,d)
  return (maxk,maxd)

def diff_schange(x,y):
  chx=schange(x)
  chy=schange(y)
  (k,ix,iy)=(0,0,0)
  #print "schange",len(chx),len(chy)
  while ix<len(chx) and iy<len(chy):
      #print ix,iy,chx[ix]+d-chy[iy]
      if chx[ix]==chy[iy]:
        #k +=1
        ix+=1
        iy +=1
      elif chx[ix]>chy[iy]:
        k +=1
        iy +=1
      elif chx[ix]<chy[iy]:
        ix +=1
        k+=1
  k +=len(chx)-ix+len(chy)-iy
  return k




def ft_pair(x,y,ops=[],maxlost=6,minleft=64):
  chx=schange(x)
  chy=schange(y)
  #print chx,"vs",chy
  if len(chx)<10:
    #print "too short",len(chx)
    return []
  k=len(chx)
  shifts=[]
  chyy=chy
  tol=min(minleft,len(chx)-maxlost)
  while k>tol:
    (k,d)=bestshift(chx,chyy)
    if k>tol:
      shifts.append(d)
    for x in chx:
       if x+d in chyy:
        chyy.remove(x+d)
  #print shifts
  return shifts
      
def ft_vec(xv,yv):
 shifts={}
 for d in xrange(-64,64):
   shifts[d]=0
 for (x,y) in zip(xv,yv):
   sh=ft_pair(x,y,minleft=3,maxlost=0)
   for s in sh:
     shifts[s]+=1
 return shifts


def PURE_FUNCTION():
	assert False, "Attempting to call pure function"


class Subgraph(object):
  def __init__(self,restrictions=ops):
    self.restrictions=restrictions.copy()
    self.inner=[]
  def is_terminal(self): PURE_FUNCTION()
  def dump(self): PURE_FUNCTION()
  def get(self,x,y,z): PURE_FUNCTION()
  def edges(self): PURE_FUNCTION()
  def rand_edge(self): PURE_FUNCTION()
  def getx(self,x):
    return self.get(x,None,None)
  def descendant(self,vec):
    if len(vec)==0: return self
    else: return self.inner[vec[0]].descendant(vec[1:])
  def deepcopy(self): PURE_FUNCTION() 
  def has_nan(self):
    if self.isnan(): return True
    for i in self.inner:
      if i.isnan():
        return True
    return False
  def setdescendant(self,vec,newval):
    if len(vec)==0:
      self=newval
    elif len(vec)==1:
      self.inner[vec[0]]=newval
    else: 
      self.inner[vec[0]].setdescendant(vec[1:],newval)
  def isnan(self):
    return False
  def all_edges(self):
    all=[([],self.restrictions)]
    for i in xrange(len(self.inner)):
      for (e,r) in self.inner[i].all_edges():
        all.append(([i]+e,r))
    #print all,len(self.inner)
    return all


class Const(Subgraph):
        def __init__(self,const,restrictions=ops):
                self.value=const
                self.inner=[]
                self.restrictions=restrictions.copy()
                if self.value>=0:
                  self.restrictions.intersection_update(ops123)
    	def get(self, x, y, z):
                if self.value==-1: return 0
                else : return self.value
	def dump(self):
                if self.value==-1: return "NaN"
                else : return self.value
        def isnan(self):
          return self.value==-1
        def edges(self):
                return 1
        def deepcopy():
                return Const(self.value,restrictions=self.restrictions)


class Var(Subgraph):
	def __init__(self, var_name = "x", restrictions=ops123):
		self.var_name = var_name
                self.inner=[]
                self.restrictions=restrictions.copy()

	def get(self, x, y, z):
		v = self.var_name
		if v == "x": return x
		if v == "y": return y
		if v == "z": return z
		assert "Bad var name"
	
	def dump(self):
		return self.var_name
        def edges(self):
                return 1
        def deepcopy():
                return Var(var_name=self.value,restrictions=self.restrictions)


class Op1(Subgraph):
	def __init__(self, op, e, restrictions=ops123):
		self.op = op
		self.inner = [e]
                self.restrictions=restrictions.copy()

	def get(self, x, y, z):
		value = self.inner[0].get(x, y, z)
		op = self.op
		v = None
		if op == "not": v = e.not64(value)
		elif op == "shr1": v = e.shr1(value)
		elif op == "shr4": v = e.shr4(value)
		elif op == "shr16": v = e.shr16(value)
		elif op == "shl1": v = e.shl1(value)
		else: assert False, "unknown operator: " + op
		return v
        def dump(self):
		return "(%s %s)" %(self.op, self.inner[0].dump())

        def edges(self):
          return 1+self.inner[0].edges()
        def deepcopy():
                return Op1(op, self.e.deepcopy(), restrictions=self.restrictions)

class Op2(Subgraph):
	def __init__(self, op, e1, e2, restrictions=ops123):
		self.op = op
		self.inner = [e1,e2]
                self.restrictions=restrictions.copy()

	def get(self, x, y, z):
		v1 = self.inner[0].get(x, y, z)
		v2 = self.inner[1].get(x, y, z)
		op = self.op
		v = None
		if op == "and": v = v1 & v2
		elif op == "or": v = v1 | v2
		elif op == "xor": v = v1 ^ v2
		elif op == "plus": v = e.plus(v1, v2)
		else: assert False, "unknown operator: " + op
		return v

	def dump(self):
		return "(%s %s %s)" %(self.op, self.inner[0].dump(), self.inner[1].dump())
        def edges(self):
          return 1+self.inner[0].edges()+self.inner[1].edges()

class If0(Subgraph):
	def __init__(self, e1, e2, e3, restrictions=ops123):
		self.inner = [e1,e2,e3]
                self.restrictions=restrictions.copy()

	def get(self, x, y, z):
		v1 = self.inner[0].get(x, y, z)
		v2 = self.inner[1].get(x, y, z)
		v3 = self.inner[2].get(x, y, z)

		if v1 == 0: return v2
		else: return v3

	def dump(self):
		return "(if0 %s %s %s)" %(self.inner[0].dump(), self.inner[1].dump(), self.inner[2].dump())
        def edges(self):
          return 1+self.inner[0].edges()+self.inner[1].edges()+self.inner[2].edges()

class Fold(Subgraph):
	def __init__(self, e1, e2, e3,restrictions=ops123):
                self.inner=(e1,e2,e3)
		self.e1 = e1  # input array
		self.e2 = e2  # initial value
		self.e3 = e3  # reduce epression
                self.restrictions=restrictions.copy()

	def get(self, x, y, z):
		res = self.e2.get(x, y, z)
		temp = self.e1.get(x, y, z)
		for i in xrange(8):
			res = self.e3.get(x, temp % 256, res)
			temp /= 256
		return res
	
	def dump(self):
		return "(fold %s %s (lambda (y z) %s))" % (self.e1.dump(), self.e2.dump(), self.e3.dump())
        def edges(self):
          return 1+self.e1.edges()+self.e2.edges()+self.e3.edges()

def objbyop(op):
  if op in ["x","y","z"]:
    return Var("x")
  elif op in ["0","1","-1"]:
    return Const(int(op))
  elif nops[op]==1:
    return Op1(op,Const(-1))
  elif nops[op]==2:
    return Op2(op,Const(-1),Const(-1))
  elif op=="fold":
    return Fold(Const(-1),Const(-1),Const(-1))
  elif op=="if0":
    return If0(Const(-1),Const(-1),Const(-1))

def insert(op,edge,graph):
  if nops[op]==0 and not graph.descendant(edge).isnan():
    return (False,[graph])
  if op not in graph.descendant(edge).restrictions:
    return (False,[graph])
  res=[]
  n=nops[op]
  #print op,n,graph.descendant(edge).restrictions, op in graph.descendant(edge).restrictions
  if n==0: n=1
  if graph.descendant(edge).isnan(): n=1
  if n==2: n=1
  for i in xrange(n):
    new=copy.deepcopy(graph)
    tail  = new.descendant(edge)
    if len(edge)>0:
      new.setdescendant(edge,objbyop(op))
    else:
      new=objbyop(op)
    #print "new",new.dump(),objbyop(op).dump()
    if nops[op]>0:
      new.setdescendant(edge+[i],tail)
    res.append(new)
  #print op,n,graph.descendant(edge).restrictions, op in graph.descendant(edge).restrictions
  graph.descendant(edge).restrictions.remove(op)
  res.append(graph)
  return (True,res) 
   
def miss(graph,xyv):
  m=0
  for (x,y) in xyv:
    m +=diff_schange(graph.getx(x),y)
  #print "miss",graph.dump(),m,graph.edges()
  return (m,graph.edges())


def queue_put(queue,el):
  mini=0
  maxi=len(queue)-1
  k=0
  if len(queue)==0:
     queue.insert(0,el)
     return queue

  while maxi>mini:
      k=(maxi+mini+1)/2
      #print mini,maxi,k
      if queue[k-1][1]>el[1]:
          maxi=k-1
      elif queue[k][1]<el[1]:
          mini=k

      else:
        mini=k
  #print "mmk",mini,maxi,k
  if queue[mini][1]<el[1]:
     queue.insert(mini+1,el)
  else :
     queue.insert(mini,el)

  #print queue
  return queue

def gen_graphs(xyv):
  g=Const(-1)
  base=[(g,miss(g,xyv))]

  for x in range(10000):
    print "step", x
    print "best graph",base[0][1],base[0][0].dump()
    if base[0][1]==0:
      print "found!"
      print base[0][0].dump()
      exit()
    #print base[0][0].dump(),base[0][0].restrictions
    #print base[0][0].all_edges()
    choices=[]
    #print "ae",base[0][0].all_edges()
    for (e,r) in base[0][0].all_edges():
      for ri in r:
        choices.append((e,ri))

    #edge=random.choice(base[0][0].all_edges())
    if len(choices)==0:
      print "==== deleted", base[0][0].dump()
      base=base[1:]
      continue

    #print "choices",choices
    (edge,op)= random.choice(choices)
    #for r in base[0][0].descendant(edge).restrictions:
    #  print "gr",goodops,r
    #  goodops.remove(r)
    #op=random.choice(goodops)
    #print "choice",edge,op
    (res,graphs)= insert(op,edge,base[0][0])
    print "choice",edge,op,res
    if res:
      base=base[1:]
      for g in graphs:
        m=miss(g,xyv)
        if m[0]==0:
          print "found"
          print g.dump()
          exit()
        #elif g.has_nan():
        queue_put(base,(g,m[0]+m[1]))
    #for g in base :
    #  print g[0].dump(),g[1]
    print "=" * 80
    
  print "last"
  for g in base :
    print g[0].dump(),g[1]
    

if __name__ == "__main__":

  k=1
  xv=[]
  yv=[]
  for i in range(200):
    x=make_rand_input(N=10,maxi=random.randint(0,64))
    if i<20:
      x=make_rand_input(N=10,maxi=16)
    if i<50:
      x=make_rand_input(N=10,maxi=32)
      #x=random.randint(0,2**32)
    xv.append(x)
    #yv.append(e.plus(e.shr16(x),e.shl1(e.shr4(x))))
    #yv.append(e.not64(e.shr4(x)) | e.plus(e.shr16(x),e.shl1(e.shr4(x))))
    #yv.append(e.not64(e.shr4(x)) | (e.shr16(x) & e.shl1(e.shl1(e.shr4(x)))))
    #yv.append(e.not64(e.shr4(x)) & (e.shr16(x) | e.shl1(e.shr4(x))))
    yv.append(e.not64(e.if0(e.shr16(e.shr16(x)), e.not64(e.shr1(x)), e.shl1(e.shr4(x)))))

  gen_graphs(zip(xv,yv))

  #shifts=ft_vec(xv,yv)
  #for s in xrange(-64,64):
  #  if shifts[s]>5:
  #    print s,shifts[s]

