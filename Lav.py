from geometry import *

class Vertex:
    def __init__(self, point):
        self.point = point
        self.next = None
        self.prev = None
        self.lav = None

        self.isAlive = True
        self.first = False
        self.processed = False

        self._isReflex = False
        self.rayDirection = None

    def __eq__(self, value):
        return self.point == value.point #pode dar problema no futuro

    def bisecting(self):
        self.isReflex()
        if self._isReflex:
            dirIn = (self.point - self.prev.point).normalize()
            dirOut = (self.point - self.next.point).normalize()
            bicectDir = (dirIn + dirOut).normalize()

        else:
            dirIn = (self.prev.point - self.point).normalize()
            dirOut = (self.next.point - self.point).normalize()
            bicectDir = (dirIn + (dirOut)).normalize()
    
        self.rayDirection =  Ray(self.point, bicectDir)
        return  self.rayDirection 

    def isReflex(self):
        # Vetores
        v_prev = self.point - self.prev.point
        v_next = self.next.point - self.point
        
        # Cross product
        cross = v_prev.x * v_next.y - v_prev.y * v_next.x
        self._isReflex = cross < 0

        return cross < 0  # CCW polygon rule

class Lav:
    def __init__(self, head:Vertex):
        self.head = head
        self.head.first = True
        self.count = 0

    def insert_vertex_between(self, vertexA:Vertex, vertexB:Vertex, newVertex:Vertex):
        newVertex.prev = vertexA
        newVertex.next = vertexB
        vertexA.next = newVertex
        vertexB.prev = newVertex
        self.count += 1

    def remove_vertex(self, vertex:Vertex):
        if self.head == vertex:
            self.head = vertex.next
            self.head.first = True
        vertex.isAlive = False
        vertex.prev.next = vertex.next
        vertex.next.prev = vertex.prev
        vertex.prev = None
        vertex.next = None
        vertex.lav = None 
        self.count -= 1

    def draw (self, ax, colorE='black',colorP='green'):
        vertex = self.head
        while True:
            vertex = vertex.next
            vertex.point.draw_seg(vertex.next.point, ax, color=colorE)
            vertex.point.draw(ax, color=colorP)
            if vertex.first:
                break


class Slav:
    def __init__(self):
        self.lavs = []

    def addLav(self, lav:Lav):
        self.lavs.append(lav)
        
    def removeLav(self, lav:Lav):
        self.lavs.remove(lav)
