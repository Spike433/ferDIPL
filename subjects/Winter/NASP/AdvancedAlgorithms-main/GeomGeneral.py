from enum import Enum

class RelativePosition(Enum):
    On=0
    RightOf=1
    LeftOf=2

class Point:
    name=None
    def __init__(self,x=0,y=0,name=None):
        self.x=x
        self.y=y
        self.name=name
    def __str__(self):
        if self.name is not None: return '{}({},{})'.format(self.name,self.x,self.y)
        else: return '({},{})'.format(self.x,self.y)
    def __eq__(self, other):
        if isinstance(other,Point): return abs(self.x-other.x)<=1e-03 and abs(self.y-other.y)<=1e-03
        else: raise Exception('type missmatch')
    def __hash__(self):
        return hash(('%.3f'%(self.x),'%.3f'%(self.y)))

class LineSegment:
    p1=Point()
    p2=Point()
    def __init__(self,p1,p2):
        self.p1=p1
        self.p2=p2
        self.dy=p2.y-p1.y
        self.dx=p2.x-p1.x
        if self.dx>0: self.dd=self.dy/self.dx
        else: self.dd=None
    def __str__(self):
        return '{}-{}'.format(self.p1,self.p2)
    def y(self,x):
        if self.dx!=0:
            return self.p1.y-(self.dy/self.dx)*self.p1.x+(self.dy/self.dx)*x
        else:
            return None
    def finv(self,e):
        if self.dx==0: return self.p1.x
        elif self.dy==0:
            if e.y!=self.p1.y: raise Exception('this is a horizontal line')
            else: return e.x
        else: return (e.y-self.p1.y+self.dd*self.p1.x)/self.dd
    def ft(self,t):
        return Point(self.p1.x+t*self.dx,self.p1.y+t*self.dy)
    def isHorizontal(self):
        return self.p1.y==self.p2.y
    def intersection(self,other):
        temp=(other.dx*self.dy-self.dx*other.dy)
        c1=other.p1.x-self.p1.x
        c2=other.p1.y-self.p1.y
        s=(other.dx*c2-c1*other.dy)/temp
        t=(self.dx*c2-c1*self.dy)/temp
        if 0<=s<=1 and 0<=t<=1: return self.ft(s)
        else: return None
    def bottomPoint(self):
        if self.p1.y<self.p2.y: return self.p1
        elif self.p2.y<self.p1.y: return self.p2
        return self.p1
    def isUpperPoint(self,e):
        if not self.isHorizontal():
            if self.p1.y<self.p2.y: return self.p2==e
            else: return self.p1==e
        else:
            if self.p1.x<self.p2.x: return self.p1==e
            else: return self.p2==e
    def isLowerPoint(self,e):
        if not self.isHorizontal():
            if self.p1.y>self.p2.y: return self.p2==e
            else: return self.p1==e
        else:
            if self.p1.x>self.p2.x: return self.p1==e
            else: return self.p2==e
    def isInteriorPoint(self,e):
        if self.dx==0:
            if e.x!=self.p1.x: return False
            else:
                if self.p1.y<self.p2.y and self.p1.y<e.y<self.p2.y: return True
                elif self.p1.y>self.p2.y and self.p1.y>e.y>self.p2.y: return True
                else: return False
        elif self.dy==0:
            if e.y!=self.p1.y: return False
            else:
                if self.p1.x<self.p2.x and self.p1.x<e.x<self.p2.x: return True
                elif self.p1.x>self.p2.x and self.p1.x>e.x>self.p2.x: return True
                else: return False
        else:
            wz=self.finv(e)
            return abs(wz-e.x)<=1e-03 and not e==self.p1 and not e==self.p2
    def position(self,point):
        if isinstance(point,Point):
            Dp=(point.x-self.p1.x)*(self.p2.y-self.p1.y)-(point.y-self.p1.y)*(self.p2.x-self.p1.x)
            if Dp>0: return RelativePosition.RightOf
            elif Dp<0: return RelativePosition.LeftOf
            else: return RelativePosition.On

def isInRange(q1,v,q2):
    if q1 is not None and q2 is not None and q1<=v<=q2: return True
    elif q1 is None and q2 is not None and v<=q2: return True
    elif q1 is not None and q2 is None and q1<=v: return True
    return False
