import math
import matplotlib.pyplot as plt



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
    

class Edge:
    def __init__(self, start: Point, end: Point,covered=False):
        self.start = start
        self.end = end
        self.crowded = False
        self.isCovered = covered

    def isIncident(self, point: Point):
        return (self.start == point) or (self.end == point)
    
    def __eq__(self, other):
        return ((self.start == other.start and self.end == other.end) or
                (self.start == other.end and self.end == other.start))
    
    def length(self):
        return self.start.distanceToPoint(self.end)
    
    def midpoint(self):
        return Point((self.start.x + self.end.x) / 2, (self.start.y + self.end.y) / 2)
    
    def circleSubdivision(self, circle: 'Circle'):
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

class Circle:
    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius

    def circleIntersects(self, other):
        dist_centers = self.center.distanceToPoint(other.center)
        return dist_centers < (self.radius + other.radius)
    
    def setRadius(self, new_radius):
        self.radius = new_radius

    def setCenter(self, new_center: Point):
        self.center = new_center

    def __eq__(self, other):
        return self.center == other.center and self.radius == other.radius
    
    def plot(self, ax, color='red', linestyle='--'):
        circle_patch = plt.Circle((self.center.x, self.center.y), self.radius, color=color, fill=False, linestyle=linestyle, linewidth=1.0)
        ax.add_patch(circle_patch)
    
class Polygon:
    def __init__(self, vertices, edges, bounding_box):
        self.vertices = vertices
        self.edges = edges
        self.subdivisions_points = []
        self.subdivisions_edges = []
        self.bounding_box = bounding_box
        self.circles = []

    def circlesColide(self, circle: Circle):
        for c in self.circles:
            if c.circleIntersects(circle):
                return True
        return False

    def generateVertexCircles(self):
        circles = []
        vertex = self.vertices
        edges = self.edges

        for v in vertex:
            distance = float('inf')
            for e in edges:
                if e.isIncident(v):
                    continue
                newDistance = e.distanceToPoint(v)
                if (newDistance < distance):
                    distance = newDistance
            c = Circle(v, distance/2)
            circles.append(c)  
        return circles 
    
    def generateEdgeSubdivisions(self):
        subdivision_points = []
        subdivision_edges = self.edges
        circles = self.circles # Assume circles have been generated and assigned to self.circles

        for circle in circles:            
            for edge in subdivision_edges:
                if edge.isCovered:
                    continue
                if edge.circleSubdivision(circle) != None:
                    sub_point = (edge.circleSubdivision(circle))
                    subdivision_points.append(sub_point)
                    if (circle.center == edge.start):
                        start_to_sub = Edge(edge.start, sub_point,covered=True)
                        sub_to_end = Edge(sub_point, edge.end)
                    else:
                        start_to_sub = Edge(edge.start, sub_point)
                        sub_to_end = Edge(sub_point, edge.end,covered=True)
                    subdivision_edges.remove(edge)
                    subdivision_edges.append(start_to_sub)
                    subdivision_edges.append(sub_to_end)
        
        self.subdivisions_points = subdivision_points
        self.subdivisions_edges = subdivision_edges
            

    def plot(self, ax, color='blue', linestyle='-'):
        for edge in self.edges:
            edge.plot(ax, color=color, linestyle=linestyle)

        ax.set_xlim(-1, 6)
        ax.set_ylim(-1, 5)
    
    
if __name__ == "__main__":
    pass