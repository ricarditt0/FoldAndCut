import matplotlib.pyplot as plt
from geometry import *

def generateVertexCircles(polygon:Polygon, rectangle:Polygon):
   return

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(6, 5))

    p1, p2, p3 = Point(1.0, 1.0), Point(4.0, 1.0), Point(2.5, 3.0)
    triangle = Polygon([p1, p2, p3])
    triangle.plot(ax, color='blue')

    p4, p5, p6, p7 = Point(0.0, 0.0), Point(5.0, 0.0), Point(5.0, 4.0), Point(0.0, 4.0)
    rectangle = Polygon([p4, p5, p6, p7])
    rectangle.plot(ax, color='black')

    plt.show()