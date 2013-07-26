'''
Created on Jun 27, 2013

@author: tel
'''
import matplotlib.pyplot as plt
import cairo
import numpy as np
from clipper import Point, Clipper, PolyType, ClipType, PolyFillType, CleanPolygons, SimplifyPolygons

def Save2D(self, fname):
    pnttoum = 1/.002834646
    f = open(fname, 'w')
    surface = cairo.PSSurface(f, 1000, 1000)
    ctx = cairo.Context(surface)
    ctx.scale(pnttoum, pnttoum)
    ctx.set_source_rgb(0, 0, 0)
    for path in self.GroupPaths(self.MidSlice()):
        ctx.move_to(*((self.hedra.get_vertex(path[0])))[0:2])
        for pnt in path[1:]:
            ctx.line_to(*(10*(self.hedra.get_vertex(pnt)))[0:2])
        ctx.fill()
        ctx.set_line_width(.01)
        ctx.stroke()
    
    surface.flush()
    surface.finish()
    f.close()

if __name__=='__main__':
    pgons = []
    for i in range(2):
        for j in range(2):
            pnts = []
            for x,y in ((0,0),(1,0),(1,1),(0,1)):
                pnts.append(Point(x+i*.75,y+j*.75))
            pgons.append(pnts)
    pnts = []
    for x,y in ((.1,.4),(.1,.6),(5,.8),(6,.2)):
        pnts.append(Point(x,y))
    pgons.append(pnts)
    toplot = []
    for poly in pgons:
        toplot = toplot + zip(*poly+[poly[0]])
    plt.plot(*toplot)
    plt.show()
    plt.clf()
    
    c = Clipper()
    s1 = []
    pft = PolyFillType.NonZero
    
    c.AddPolygon(pgons[0], PolyType.Subject)
    c.AddPolygons(pgons[1:-1], PolyType.Clip)
    result1 = c.Execute(ClipType.Union, s1, pft, pft)
    
    c = Clipper()
    s2 = []
    
    c.AddPolygon(s1[0], PolyType.Subject)
    c.AddPolygon(pgons[-1], PolyType.Clip)
    result2 = c.Execute(ClipType.Union, s2, pft, pft)
    
    toplot = []
    for poly in s1:
        toplot = toplot + zip(*poly+[poly[0]])
    plt.plot(*toplot)
    plt.show()
    plt.clf()
    
    toplot = []
    for poly in s2:
        toplot = toplot + zip(*poly+[poly[0]])
    plt.plot(*toplot)
    plt.show()