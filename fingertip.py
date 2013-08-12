from consts import LAST
import random
import expression as e

random.seed(0)

ops=["0","1","x","shl1","shr1","shr4","shr16","not","and","or","xor","plus","if0"]
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


