from GeomGeneral import LineSegment,RelativePosition

def SimpleConvexHull(Pp):
    ch=[]
    for pi in Pp:
        for pj in [i for i in Pp if i is not pi]:
            v=True
            ls=LineSegment(pi,pj)
            for pk in [i for i in Pp if i not in [pi,pj]]:
                if ls.position(pk) is RelativePosition.LeftOf:
                    v=False
                    break
            if v: ch.append(ls)
    return ch

def ConvexHull(Pp):
    hPp=sorted(Pp,key=lambda p:p.x)
    lu=[hPp[0],hPp[1]]
    for i in range(2,len(hPp)):
        lu.append(hPp[i])
        while len(lu)>2 and LineSegment(lu[-3],lu[-2]).position(lu[-1]) is RelativePosition.LeftOf:
            lu.pop(-2)
    ll=[hPp[-1],hPp[-2]]
    for i in range(3,len(hPp)+1):
        ll.append(hPp[-i])
        while len(ll)>2 and LineSegment(ll[-3],ll[-2]).position(ll[-1]) is RelativePosition.LeftOf:
            ll.pop(-2)
    ll.pop(0)
    ll.pop(-1)
    return lu+ll


