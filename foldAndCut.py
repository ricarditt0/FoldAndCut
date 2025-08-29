import matplotlib.pyplot as plt
from geometry import *


if __name__ == "__main__":
   fig, ax = plt.subplots(figsize=(6, 5))


   p1, p2, p3 = Point(1.0, 1.0), Point(4.0, 1.0), Point(2.5, 3.0)
   e1, e2, e3 = Edge(p1, p2), Edge(p2, p3), Edge(p3, p1)
   p4, p5, p6, p7 = Point(0.0, 0.0), Point(5.0, 0.0), Point(5.0, 4.0), Point(0.0, 4.0)
   e4, e5, e6, e7 = Edge(p4, p5), Edge(p5, p6), Edge(p6, p7), Edge(p7, p4)
   bounding_box = [p4, p5, p6, p7]

   triangle = Polygon([p1, p2, p3, p4, p5, p6, p7], [e1, e2, e3, e4, e5, e6, e7], bounding_box)
   triangle.plot(ax, color='black')

   triangle.circles = triangle.generateVertexCircles()
   Circles = triangle.circles
   for circle in Circles:
      circle.plot(ax, color='red', linestyle='--')

   triangle.generateEdgeSubdivisions()
   edges = triangle.subdivisions_edges
   for edge in edges:
      if edge.isCovered:
         edge.plot(ax, color='orange', linestyle='-')
      else:
         edge.plot(ax, color='blue', linestyle='-')


   plt.show()