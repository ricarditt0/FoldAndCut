import math
import matplotlib.pyplot as plt



class Point:
    def __init__(self, x, y,vertexCricle:'Circle'=None):
        self.x = x
        self.y = y
        self.vertexCircle = vertexCricle

    def distanceToPoint(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def __eq__(self, other):
        if other is None:
            return False
        return self.x == other.x and self.y == other.y
    
    def plot(self, ax, color='purple', linestyle='None'):
        ax.plot(self.x, self.y, marker='o', color=color, linestyle=linestyle)

class Circle:
    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius

    def circleIntersects(self, other):
        eps=1e-9
        dist_centers = self.center.distanceToPoint(other.center)
        return dist_centers < (self.radius + other.radius - eps)
    
    def setRadius(self, new_radius):
        self.radius = new_radius

    def setCenter(self, new_center: Point):
        self.center = new_center

    def __eq__(self, other):
        return self.center == other.center and self.radius == other.radius
    
    def plot(self, ax, color='red', linestyle='--'):
        circle_patch = plt.Circle((self.center.x, self.center.y), self.radius, color=color, fill=False, linestyle=linestyle, linewidth=1.0)
        ax.add_patch(circle_patch)

class Edge:
    def __init__(self, start:Point, end:Point,covered=False,edgeCircle:Circle=None):
        self.start = start
        self.end = end
        self.crowded = False
        self.isCovered = covered
        self.edgeCircle = edgeCircle

    def isIncident(self, point: Point):
        return (self.start == point) or (self.end == point)
    
    def __eq__(self, other):
        return ((self.start == other.start and self.end == other.end) or
                (self.start == other.end and self.end == other.start))

    def length(self):
        return self.start.distanceToPoint(self.end)
    
    def midpoint(self):
        return Point((self.start.x + self.end.x) / 2, (self.start.y + self.end.y) / 2)
    
    def makeCircle(self):
        midpoint = self.midpoint()
        radius = self.length() / 2
        self.edgeCircle = Circle(midpoint, radius)
    
    def circleSubdivision(self, circle: Circle):
        #vector
        vector_x = 0
        vector_y = 0
        subvisoinPoint = None
        if self.start == circle.center:
            vector_x = self.end.x - self.start.x
            vector_y = self.end.y - self.start.y
            subvisoinPoint = Point(self.start.x + vector_x * circle.radius / math.hypot(vector_x, vector_y),
                                   self.start.y + vector_y * circle.radius / math.hypot(vector_x, vector_y))
        elif self.end == circle.center:
            vector_x = self.start.x - self.end.x
            vector_y = self.start.y - self.end.y
            subvisoinPoint = Point(self.end.x + vector_x * circle.radius / math.hypot(vector_x, vector_y),
                                   self.end.y + vector_y * circle.radius / math.hypot(vector_x, vector_y))

        return subvisoinPoint
    
    def plot(self, ax, color='green', linestyle='-'):
        ax.plot([self.start.x, self.end.x], [self.start.y, self.end.y], color=color, linestyle=linestyle, linewidth=1.5)
    
    def distanceToPoint(self, point: Point):

        closest_x, closest_y = 0, 0

        #vector start to end
        start_endx = self.end.x - self.start.x
        start_endy = self.end.y - self.start.y

        #vector start to point
        start_pointx = point.x - self.start.x
        start_pointy = point.y - self.start.y

        #scalar projection of start_point onto start_end normalized
        t = (start_pointx * start_endx + start_pointy * start_endy) / (start_endx * start_endx + start_endy * start_endy)
        if t < 0:
            closest_x, closest_y = self.start.x, self.start.y
        elif t > 1:
            closest_x, closest_y = self.end.x, self.end.y
        else:
            closest_x = self.start.x + t * start_endx
            closest_y = self.start.y + t * start_endy

        dx = point.x - closest_x
        dy = point.y - closest_y

        return math.hypot(dx, dy)
    
class Polygon:
    def __init__(self, vertices, edges, bounding_box):
        self.vertices = vertices
        self.edges = edges
        self.subdivisions_points = []
        self.subdivisions_edges = []
        self.bounding_box = bounding_box
        
    
    def getEdgesCircles(self):
        circles = []
        for edge in self.subdivisions_edges:
            if edge.edgeCircle is not None:
                circles.append(edge.edgeCircle)
        return circles
    
    def getVertexCircles(self):
        circles = []
        for vertex in self.vertices:
            if vertex.vertexCircle is not None:
                circles.append(vertex.vertexCircle) 
        return circles
    
    def getCircles(self):
        return self.getVertexCircles() + self.getEdgesCircles()

    def markCrowdedEdges(self):
        count = 0
        circles = self.getCircles()
        for edge in self.subdivisions_edges:
            if edge.isCovered:
                continue
            for circle in circles:
                if edge.edgeCircle.circleIntersects(circle) and edge.edgeCircle != circle:
                    edge.crowded = True
                    count += 1
                    break
        return count 

    def generateVertexCircles(self):
        for vertex in self.vertices:
            distance = float('inf')
            for edge in self.edges:
                if edge.isIncident(vertex):
                    continue
                newDistance = edge.distanceToPoint(vertex)
                if (newDistance < distance):
                    distance = newDistance
            c = Circle(vertex, distance/2)
            vertex.vertexCircle = c
    
    def generateEdgeSubdivisions(self):
        subdivision_edges = self.edges
        circles = self.getCircles()

        for circle in circles:            
            for edge in subdivision_edges:
                if edge.isCovered:
                    continue
                if edge.circleSubdivision(circle) != None:
                    sub_point = (edge.circleSubdivision(circle))
                    self.subdivisions_points.append(sub_point)
                    if (circle.center == edge.start):
                        start_to_sub = Edge(edge.start, sub_point,covered=True)
                        sub_to_end = Edge(sub_point, edge.end)
                    else:
                        start_to_sub = Edge(edge.start, sub_point)
                        sub_to_end = Edge(sub_point, edge.end,covered=True)
                    subdivision_edges.remove(edge)
                    subdivision_edges.append(start_to_sub)
                    subdivision_edges.append(sub_to_end)
        
        self.subdivisions_edges = subdivision_edges[:]
            
    def generateEdgeCircles(self):
        for edge in self.subdivisions_edges:
            if edge.isCovered:
                continue
            edge.makeCircle()
                

    def splitCrowdedEdges(self):
        while self.markCrowdedEdges():
            new_subdivision_edges = []
            # marcar crowded
            
            for edge in self.subdivisions_edges:
                if edge.isCovered:
                    new_subdivision_edges.append(edge)
                    continue
                
                if edge.crowded:
                    midpoint = edge.midpoint()
                    self.subdivisions_points.append(midpoint)

                    start_to_mid = Edge(edge.start, midpoint)
                    start_to_mid.makeCircle()
                    mid_to_end = Edge(midpoint, edge.end)
                    mid_to_end.makeCircle()

                    new_subdivision_edges.extend([start_to_mid, mid_to_end])
                else:
                    new_subdivision_edges.append(edge)

            self.subdivisions_edges = new_subdivision_edges[:]





    def plot(self, ax, color='blue', linestyle='-'):
        for edge in self.edges:
            edge.plot(ax, color=color, linestyle=linestyle)

        ax.set_xlim(-1, 6)
        ax.set_ylim(-1, 5)
    
    
if __name__ == "__main__":
    pass