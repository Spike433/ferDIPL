import unittest
from ConvexHull import SimpleConvexHull,ConvexHull
from IntervalTree import IntervalTree
from OneDRangeTree import BinaryTreeWithLeafValues,OneDRangeQuery
from PlaneSweepingLSIntersection import PlaneSweepLSIntersection
from PriorityTree import PriorityTree
from GeomGeneral import Point,LineSegment
from SegmentTree import SegmentTree

class SimpleBinaryTreeCases(unittest.TestCase):
    def test_ConvexHull(self):
        p10=Point(2,10,'p10')
        p8=Point(2.5,11,'p8')
        p12=Point(3,10.5,'p12')
        p7=Point(3.1,8,'p7')
        p13=Point(3.6,9.6,'p13')
        p4=Point(4,11,'p4')
        p6=Point(4.2,8.4,'p6')
        p2=Point(4.5,13,'p2')
        p1=Point(5,15,'p1')
        p5=Point(5.2,10,'p5')
        p3=Point(5.5,11.2,'p3')
        p15=Point(6,10.5,'p15')
        p11=Point(6.5,14,'p11')
        p14=Point(6.6,8,'p14')
        p9=Point(7,11.6,'p9')
        Pp=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15]
        r1=SimpleConvexHull(Pp)
        #for ls in r1: print(ls)
        #print('----')
        r2=ConvexHull(Pp)
        #for ls in r2: print(ls)

    def test_IntervalQuery(self):
        I=[((1,5),0),((2,17),0),((3,7),0),((4,11),0),((8,13),0),((10,14),0),((12,19),0),((2,20),1.5),((5,11.5),0.7)]
        tau=IntervalTree(I)
        ivres=tau.IntervalQuery(11.2,12.4,-1,1)
        #print(ivres)

    def test_OneDRangeQuery(self):
        tau=BinaryTreeWithLeafValues(rootValue=170)
        tau.insert([163,189,159,168,176,196,155,161,165,169,173,179,191,198])
        rv=OneDRangeQuery(tau,165,184)
        vls=sorted(rv,key=lambda i:i.value)
        #for i in vls: print(i.value)
        #print('----')
        tau=BinaryTreeWithLeafValues(Pp=[160,163,169,172,173,180,188,192,193,198])
        rv=OneDRangeQuery(tau,170,189)
        vls=sorted(rv,key=lambda i:i.value)
        #for i in vls: print(i.value)

    def test_PlaneLineSweeping(self):
        ls1=LineSegment(p1=Point(2,2),p2=Point(10,10))
        ls2=LineSegment(p1=Point(2,10),p2=Point(10,2))
        ls3=LineSegment(p1=Point(6,8),p2=Point(6,4))
        ls4=LineSegment(p1=Point(9,7),p2=Point(10,4))
        ls5=LineSegment(p1=Point(6,6),p2=Point(20,6))
        ls6=LineSegment(p1=Point(8,6.5),p2=Point(13,6.5))
        ls7=LineSegment(p1=Point(6,1),p2=Point(10,4))
        ls8=LineSegment(p1=Point(7,5),p2=Point(11,5))
        ls9=LineSegment(p1=Point(0,3),p2=Point(15,3))
        I=PlaneSweepLSIntersection([ls8,ls1,ls6,ls2,ls3,ls4,ls9,ls7,ls5])
        #print(I)

    def test_PrioTreeQuery(self):
        Pp=[(10,9.5),(11,1.8),(11.1,5.7),(2,10),(3,7),(4,2),(5,10.5),(5.5,5),(7,8),(8,2.1),(8.1,4.8),(12,1.5)]
        tau=PriorityTree(Pp)
        rv=tau.Query(15,1,4)

    def test_TwoDRangeQuery(self):
        from TwoDRangeTree import BinaryTreeWithLeafValues
        Pp=[{'point':(2,10)},{'point':(3,7)},{'point':(4,2)},{'point':(5,10.5)},{'point':(5.5,5)},
            {'point':(7,8)},{'point':(8,2.1)},{'point':(8.1,4.8)},{'point':(10,9.5)},{'point':(11,1.8)},
            {'point':(11.1,5.7)}]
        tau=BinaryTreeWithLeafValues(Pp)
        rv=tau.TwoDRangeQuery(1,5,4,15)
        #for v in rv: print(v[0]['point'])

    def test_SegmentTree(self):
        ls1=LineSegment(p1=Point(2,2),p2=Point(10,3))
        ls2=LineSegment(p1=Point(3,3),p2=Point(11,4))
        ls3=LineSegment(p1=Point(4,4),p2=Point(12,5))
        ls4=LineSegment(p1=Point(2,10),p2=Point(5,5))
        ls5=LineSegment(p1=Point(6,10),p2=Point(6,5))
        st=SegmentTree([ls1,ls2,ls3,ls4,ls5])
        res=st.query(((5.5,9),(4,9)))
        #for ls in res: print(ls)
        self.assertTrue(len(res)==2)

if __name__ == '__main__':
    unittest.main()
