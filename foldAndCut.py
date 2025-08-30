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

   triangle.generateVertexCircles()
   
   triangle.generateEdgeSubdivisions() # <----

   triangle.generateEdgeCircles()
   print(len(triangle.subdivisions_edges))

   triangle.splitCrowdedEdges()
   print(len(triangle.subdivisions_edges))
   triangle.markCrowdedEdges()

   circles = triangle.getVertexCircles()
   for circle in circles:
      circle.plot(ax, color='red')

   edges = triangle.subdivisions_edges
   for edge in edges:
      if edge.crowded:
         edge.plot(ax, color='orange', linestyle='-')
      else:
         edge.plot(ax, color='blue', linestyle='-')

   vertexes = triangle.subdivisions_points
   for vertex in vertexes:
      vertex.plot(ax, color='black')

   circles = triangle.getEdgesCircles()

   for circle in circles:
      circle.plot(ax, color='green')

   # circles[8].plot(ax,color = 'green')
   # circles[9].plot(ax,color = 'green')
   # print(circles[8].circleIntersects(circles[9]))



   plt.show()