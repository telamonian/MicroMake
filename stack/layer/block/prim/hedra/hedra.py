'''
Created on Jun 5, 2013

@author: tel
'''
import cairo, itertools 
import numpy as np
import scipy.spatial as spatial
import pyPolyCSG as csg

from transmat import rotation_matrix, translation_matrix

class Hedra(object):
    def __init__(self):
        self.hedra = csg.polyhedron()
    
    def Union(self, other):
        '''union of two hedra'''
        self.hedra = self.hedra + other.hedra

    def Diff(self, other):
        '''difference of two hedra'''
        self.hedra = self.hedra - other.hedra
        
    def SymDiff(self, other):
        '''symmetric difference of two hedra
        equivalent to the difference of the union and the intersection'''
        self.hedra = self.hedra ^ other.hedra
        
    def Intersect(self, other):
        '''intersection of two hedra'''
        self.hedra = self.hedra * other.hedra
    
    def GetConnect(self):
        connect = []
        botverts = []
        facedict = {}
        for i,vert in enumerate(self.hedra.get_vertices()):
            if np.allclose(0,vert[2]):
                botverts.append(i)
        for face in [self.hedra.get_face(i) for i in range(self.hedra.num_faces())]:
            for vert in face:
                facedict[vert] = facedict.get(vert, []) + [face]
        for bvert,faces in [pair for pair in facedict.items() if pair[0] in botverts]:
            countdict = {}
            for vert in [vert for face in faces for vert in face if vert!=bvert]:
                countdict[vert] = countdict.get(vert, 0) + 1
            for vert,count in [pair for pair in countdict.items() if pair[1] > 1]:
                connect.append((bvert, vert))
        return connect
    
    def Slice(self, a=0, b=0, c=1, d=.5):
        norm0 = np.array((a,b,c))
        for face in [self.hedra.get_face(i) for i in range(self.hedra.num_faces())]:
            for perm in itertools.permutations(face, 3):
                vec0 = self.hedra.get_vertex(perm[1]) - self.hedra.get_vertex(perm[0])
                vec1 = self.hedra.get_vertex(perm[2]) - self.hedra.get_vertex(perm[0])
                if not np.allclose(np.array((0,0,0)), vec0.cross(vec1)):
                    norm1 = vec0.cross(vec1)
                    break
            intervec = norm0.cross(norm1)
            d1 = self.hedra.get_vertex(perm[0]).dot(norm1)
            np.linalg.solve((norm0[1:3], norm1[1:3]), (d, d1))
            #not done
    
    def MidSlice(self):
        connects = []
        for face in [self.hedra.get_face(i) for i in range(self.hedra.num_faces())]:
            verts = np.array([self.hedra.get_vertex(i) for i in face])
            if not np.allclose(verts[0,2], verts[1:,2]):
                try:
                    hull = spatial.ConvexHull(verts[:,1:3], qhull_options='')
                except:
                    hull = spatial.ConvexHull(verts[:,::2], qhull_options='')
                connect = []
                for simplex in hull.simplices:
                    if not np.allclose(verts[simplex[0]][2], verts[simplex[1]][2]):
                        if verts[simplex[0]][2] < verts[simplex[1]][2]:
                            connect.append(face[simplex[0]])
                        else:
                            connect.append(face[simplex[1]])
                connects.append(connect)
        return connects
            
    def Save2D(self, fname):
        f = open(fname, 'w')
        surface = cairo.PSSurface(f, 100, 100)
        ctx = cairo.Context(surface)
        ctx.set_source_rgb(0, 0, 0)
        for path in self.GroupPaths(self.MidSlice()):
            ctx.move_to(*self.hedra.get_vertex(path[0][0])[0:2])
            ctx.line_to(*self.hedra.get_vertex(path[0][1])[0:2])
            for start,end in path[1:]:
                ctx.line_to(*self.hedra.get_vertex(end)[0:2])
            ctx.close_path()
            ctx.set_line_width(.1)
            ctx.stroke()
            ctx.fill()
        
        surface.flush()
        surface.finish()
        f.close()
    def Transform(self, mat):
        '''transform hedra based on a 4x4 matrix'''
        flatmat = [j for i in mat for j in i]
        self.hedra = self.hedra.mult_matrix_4(flatmat)
        
    def RetTransform(self, mat):
        flatmat = [j for i in mat for j in i]
        return self.hedra.mult_matrix_4(flatmat)
        
    @staticmethod
    def OverlaySegMat(seg2, seg1):
        '''returns 4x4 transformation matrix that will overlay seg1 on seg2. each seg is a line segment represented by a list of two points'''
        vec1 = np.array(seg1[1]) - np.array(seg1[0])
        vec2 = np.array(seg2[1]) - np.array(seg2[0])
        ang = np.arccos(np.dot(vec1, vec2)/(np.sqrt(np.dot(vec1, vec1))*np.sqrt(np.dot(vec2, vec2))))
        if np.allclose(vec1,vec2):
            axis = (0,0,1)
        else:
            axis = np.cross(vec1, vec2)
        trans = np.array(seg2[0]) - np.array(seg1[0])
        return  translation_matrix(trans).dot(rotation_matrix(ang, axis, point=seg1[0]))
    
    @staticmethod
    def RotatePointMat(ang, pnt, seg1=None, seg2=None):
        '''returns 4x4 transformation matrix that will rotate by ang (in radians) about pnt. 
        line segments seg1 and seg2 may optionally be specified in order to fix the axis of rotation as their cross product.
        each seg is a line segment represented by a list of two points. otherwise, rotation occurs about the z axis'''
        if seg1!=None and seg2!=None:
            vec1 = np.array(seg1[1]) - np.array(seg1[0])
            vec2 = np.array(seg2[1]) - np.array(seg2[0])
            if np.allclose(vec1,vec2):
                axis = (0,0,1)
            else:
                axis = np.cross(vec1, vec2)
        else:
            axis = (0,0,1)
        return rotation_matrix(ang, axis, point=pnt)
    
    @staticmethod
    def TranslateMat(pnt1, pnt2):
        '''returns 4x4 transformation matrix that translates from pnt1 to pnt2'''
        vec = np.array(pnt2) - np.array(pnt1)
        return translation_matrix(vec)
    
    @staticmethod
    def Midpoint(seg):
        return (np.array(seg[0]) + np.array(seg[1]))/2
    
    '''
    deprecated methods left in to help with unit testing
    '''
    
    def SegToSeg(self, seg1, seg2, offang=0):
        '''define a transformation based on moving one line segment to overlap with another, then apply it'''
        tmat = [a for b in Hedra.SegTransform(seg1, seg2, offang).tolist() for a in b]  #format transformation matrix as flat row-major list
        self.hedra = self.hedra.mult_matrix_4(tmat)
    
    def MoveToPos(self, inletnum=None, offang=0):
        '''position self based on line seg in self.loc'''
        try:
            self.SegToSeg(self.GetInlet(inletnum), self.GetPrevOutlet(self.outnum), offang)
        except AttributeError:
            self.SegToSeg(self.GetInlet(inletnum), self.loc, offang)
    
    @staticmethod
    def SegTransform(seg1, seg2, offang=0):
        vec1 = np.array(seg1[1]) - np.array(seg1[0])
        vec2 = np.array(seg2[1]) - np.array(seg2[0])
        ang = np.arccos(np.dot(vec1, vec2)/(np.sqrt(np.dot(vec1, vec1))*np.sqrt(np.dot(vec2, vec2))))
        if np.allclose(vec1,vec2):
            axis = (0,0,1)
        else:
            axis = np.cross(vec1, vec2)
        trans = np.array(seg2[0]) - np.array(seg1[0])
        #perpunittrans = .1*(np.array((-vec2[1],vec2[0],vec2[2]))/(np.sqrt(np.sum(vec2**2))))
        return rotation_matrix(offang, axis, point=Hedra.Midpoint(seg2)).dot(translation_matrix(trans)).dot(rotation_matrix(ang, axis, point=seg1[0]))#.dot(translation_matrix(perpunittrans))
    
    @staticmethod
    def GroupPaths(paths):
        lastp = []
        groups = []
        for path in paths:
            try:
                i = lastp.index(path[0])
                groups[i].append(path)
                lastp[i] = path[1]
            except ValueError:
                groups.append([path])
                lastp.append(path[1])
        return groups