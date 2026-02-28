import matplotlib.pyplot as plt

class Point:
    def __init__(self, x: float, y: float, isPoint=True):
        self.x = x
        self.y = y
        self.isPoint = True

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, isPoint=False)
    
    def __mul__(self, scalar: float):
        return Point(self.x * scalar, self.y * scalar)
    
    def __hash__(self):
        return hash((self.x, self.y))

    def almost_equal(p1, p2, eps=1e-6):
        return abs(p1.x - p2.x) < eps and abs(p1.y - p2.y) < eps

    def normalize(self):
        length = (self.x ** 2 + self.y ** 2) ** 0.5
        if length == 0:
            return Point(0, 0)
        return Point(self.x / length, self.y / length)
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def draw (self, ax, color='black'):
        ax.plot(self.x, self.y, marker='o', color=color)

    def draw_seg(self, point, ax, color='black'):
        ax.plot([self.x, point.x], [self.y, point.y], color=color)

class Edge:
    def __init__(self, ini:Point, end:Point):
        self.ini = ini
        self.end = end
    
    def length(self):
        return ((self.end.x - self.ini.x) ** 2 + (self.end.y - self.ini.y) ** 2) ** 0.5

    def __eq__(self, value):
        return (self.ini == value.ini and self.end == value.end) or (self.ini == value.end and self.end == value.ini)

    def __repr__(self):
        return f"Edge star({self.ini}), end({self.end})"
    
    def draw(self, ax, color='black'):
        ax.plot([self.ini.x, self.end.x], [self.ini.y, self.end.y], color=color)

class Ray:
    def __init__(self, origin:Point, direction:Point):
        self.origin = origin
        self.direction = direction.normalize()
        self.isRay = True

    def intersect(self, other):
        # Resolve P1 + t1*b1 = P2 + t2*b2
        p1, b1 = self.origin, self.direction
        p2, b2 = other.origin, other.direction
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        det = b1.x * b2.y - b1.y * b2.x
        if det == 0:
            print("No intersection: parallel lines")
            return None  # Parallel lines

        t1 = (dx * b2.y - dy * b2.x) / det
        t2 = (dx * b1.y - dy * b1.x) / det

        if t1 < 0 or t2 < 0:
            print("No intersection: t1 =", t1, ", t2 =", t2)
            return None  # Intersection is behind the ray origin
        
        else:
            intersection_point = Point(p1.x + t1 * b1.x, p1.y + t1 * b1.y)
            return intersection_point , t1, t2


    def draw(self, ax, length=10.0, color='black'):
        end_point = self.origin + self.direction.normalize() * length
        ax.plot([self.origin.x, end_point.x], [self.origin.y, end_point.y], color=color)

if __name__ == "__main__":
    pass