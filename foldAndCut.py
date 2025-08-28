import matplotlib.pyplot as plt
from geometry import *

def generateVertexCircles(polygon:Polygon, rectangle:Polygon):
   circles = []
   vertex = polygon.vertices + rectangle.vertices
   edges = polygon.edges + rectangle.edges

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

def generateEdgeCircles():
   pass

if __name__ == "__main__":
   fig, ax = plt.subplots(figsize=(6, 5))

   p1, p2, p3 = Point(1.0, 1.0), Point(4.0, 1.0), Point(2.5, 3.0)
   triangle = Polygon([p1, p2, p3])
   triangle.plot(ax, color='blue')

   p4, p5, p6, p7 = Point(0.0, 0.0), Point(5.0, 0.0), Point(5.0, 4.0), Point(0.0, 4.0)
   rectangle = Polygon([p4, p5, p6, p7])
   rectangle.plot(ax, color='black')

   Circles = generateVertexCircles(triangle, rectangle)
   for circle in Circles:
      circle.plot(ax, color='red', linestyle='--')

   edges = triangle.edges + rectangle.edges


   for edge in edges:
      for circle in Circles:
         if edge.circleSubdivision(circle) != None:
            sub_point = (edge.circleSubdivision(circle))
            sub_point.plot(ax, color='green', linestyle='None')
            


   plt.show()