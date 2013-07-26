'''
Created on Jun 5, 2013

@author: tel
'''
import cairo, itertools 
import numpy as np
import scipy.spatial as spatial
import pyPolyCSG as csg

from transmat import rotation_matrix, translation_matrix

#    def GetConnect(self):
#        connect = []
#        botverts = []
#        facedict = {}
#        for i,vert in enumerate(self.hedra.get_vertices()):
#            if np.allclose(0,vert[2]):
#                botverts.append(i)
#        for face in [self.hedra.get_face(i) for i in range(self.hedra.num_faces())]:
#            for vert in face:
#                facedict[vert] = facedict.get(vert, []) + [face]
#        for bvert,faces in [pair for pair in facedict.items() if pair[0] in botverts]:
#            countdict = {}
#            for vert in [vert for face in faces for vert in face if vert!=bvert]:
#                countdict[vert] = countdict.get(vert, 0) + 1
#            for vert,count in [pair for pair in countdict.items() if pair[1] > 1]:
#                connect.append((bvert, vert))
#        return connect
#    
#    def Slice(self, a=0, b=0, c=1, d=.5):
#        norm0 = np.array((a,b,c))
#        for face in [self.hedra.get_face(i) for i in range(self.hedra.num_faces())]:
#            for perm in itertools.permutations(face, 3):
#                vec0 = self.hedra.get_vertex(perm[1]) - self.hedra.get_vertex(perm[0])
#                vec1 = self.hedra.get_vertex(perm[2]) - self.hedra.get_vertex(perm[0])
#                if not np.allclose(np.array((0,0,0)), vec0.cross(vec1)):
#                    norm1 = vec0.cross(vec1)
#                    break
#            intervec = norm0.cross(norm1)
#            d1 = self.hedra.get_vertex(perm[0]).dot(norm1)
#            np.linalg.solve((norm0[1:3], norm1[1:3]), (d, d1))
#            #not done
#    
#    def MidSlice(self):
#        connects = []
#        for face in [self.hedra.get_face(i) for i in range(self.hedra.num_faces())]:
#            verts = np.array([self.hedra.get_vertex(i) for i in face])
#            if not np.allclose(verts[0,2], verts[1:,2]):
#                try:
#                    hull = spatial.ConvexHull(verts[:,1:3], qhull_options='')
#                except:
#                    hull = spatial.ConvexHull(verts[:,::2], qhull_options='')
#                connect = []
#                for simplex in hull.simplices:
#                    if not np.allclose(verts[simplex[0]][2], verts[simplex[1]][2]):
#                        if verts[simplex[0]][2] < verts[simplex[1]][2]:
#                            connect.append(face[simplex[0]])
#                        else:
#                            connect.append(face[simplex[1]])
#                connects.append(connect)
#        return connects
#            
#    def Save2D(self, fname):
#        f = open(fname, 'w')
#        surface = cairo.PSSurface(f, 1000, 1000)
#        ctx = cairo.Context(surface)
#        ctx.set_source_rgb(0, 0, 0)
#        for path in self.GroupPaths(self.MidSlice()):
#            ctx.move_to(*((self.hedra.get_vertex(path[0])))[0:2])
#            for pnt in path[1:]:
#                ctx.line_to(*(10*(self.hedra.get_vertex(pnt)))[0:2])
#            ctx.fill()
#            ctx.set_line_width(.01)
#            ctx.stroke()
#        
#        surface.flush()
#        surface.finish()
#        f.close()
#        
#    @staticmethod
#    def GroupPaths(paths):
#        groups = []
#        pset = set([point for points in paths for point in points])
#        pdict = {}
#        for path in paths:
#            pdict[path[0]] = pdict.get(path[0], []) + [path[1]]
#            pdict[path[1]] = pdict.get(path[1], []) + [path[0]]
#        while len(pset) > 0:
#            group = [pset.pop()]
#            last = group[0]
#            now = pdict[group[0]][0]
#            while now!=group[0]:
#                group.append(now)
#                pset.remove(now)
#                tnow = pdict[now][0] if pdict[now][0]!=last else pdict[now][1]
#                last = now
#                now = tnow
#            groups.append(group)
#        return groups