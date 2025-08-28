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
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
        self.crowded = False
        self.isCovered = False

    def isIncident(self, point: Point):
        return (self.start == point) or (self.end == point)
    
    def __eq__(self, other):
        return ((self.start == other.start and self.end == other.end) or
                (self.start == other.end and self.end == other.start))
    
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
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = self.edges()
        self.subdivisions_points = []
        self.subdivisions_edges = []
    
    def edges(self):
        edges = []
        n = len(self.vertices)
        for i in range(n):
            start = self.vertices[i]
            end = self.vertices[(i + 1) % n]
            new = Edge(start, end)
            edges.append(new)
        return edges
    
    def plot(self, ax, color='blue', linestyle='-'):
        coords = [(v.x, v.y) for v in self.vertices]
        p = plt.Polygon(coords, fill=None, edgecolor=color, linestyle=linestyle, linewidth=1.5)
        ax.add_patch(p)

        ax.set_xlim(-1, 6)
        ax.set_ylim(-1, 5)
    
    
if __name__ == "__main__":

    fig, ax = plt.subplots(figsize=(6, 5))

    p1, p2, p3 = Point(1.0, 1.0), Point(4.0, 1.0), Point(2.5, 3.0)
    triangle = Polygon([p1, p2, p3])
    triangle.plot(ax, color='blue')

    p4, p5, p6, p7 = Point(0.0, 0.0), Point(5.0, 0.0), Point(5.0, 4.0), Point(0.0, 4.0)
    rectangle = Polygon([p4, p5, p6, p7])
    rectangle.plot(ax, color='black')


    plt.show()