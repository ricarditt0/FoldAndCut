import matplotlib.pyplot as plt
from geometry import *
from scipy.spatial import Delaunay
import numpy as np
import math

def voronoi_vertices_from_delaunay(points):
   """
    points: lista de pontos (x,y)
    return: lista de (vx, vy, simplex_indices)
   """
   aux = [(p.x, p.y) for p in points]

   pts = np.array(aux)
   tri = Delaunay(pts)

   vertices = []
   for simplex in tri.simplices:
      (i, j, k) = simplex
      A = pts[i]
      B = pts[j]
      C = pts[k]

      # circuncentro do triângulo ABC
      d = 2 * (A[0]*(B[1]-C[1]) +
              B[0]*(C[1]-A[1]) +
              C[0]*(A[1]-B[1]))

      if abs(d) < 1e-12:
         continue

      ux = ((np.linalg.norm(A)**2)*(B[1]-C[1]) +
           (np.linalg.norm(B)**2)*(C[1]-A[1]) +
           (np.linalg.norm(C)**2)*(A[1]-B[1])) / d

      uy = ((np.linalg.norm(A)**2)*(C[0]-B[0]) +
           (np.linalg.norm(B)**2)*(A[0]-C[0]) +
           (np.linalg.norm(C)**2)*(B[0]-A[0])) / d

      vertices.append((Point(ux,uy), (i, j, k)))

   return vertices

def weighted_voronoi_vertex(c1, c2, c3):
    """
    Calcula o vértice do diagrama de potência (weighted Voronoi)
    definido por 3 círculos c1, c2, c3.
    Retorna (px, py) se existir solução válida.
    """
    # Montar o sistema linear:
    # 2*(c2 - c1)·p = (|c2|^2 - r2^2) - (|c1|^2 - r1^2)
    # 2*(c3 - c1)·p = (|c3|^2 - r3^2) - (|c1|^2 - r1^2)

    A = np.array([
        [2*(c2.center.x - c1.center.x), 2*(c2.center.y - c1.center.y)],
        [2*(c3.center.x - c1.center.x), 2*(c3.center.y - c1.center.y)]
    ])
    b = np.array([
        (c2.center.x**2 + c2.center.y**2 - c2.radius**2) - (c1.center.x**2 + c1.center.y**2 - c1.radius**2),
        (c3.center.x**2 + c3.center.y**2 - c3.radius**2) - (c1.center.x**2 + c1.center.y**2 - c1.radius**2)
    ])

    if abs(np.linalg.det(A)) < 1e-9:
        return None  # círculos alinhados ou degenerados

    p = np.linalg.solve(A, b)
    return (Point(p[0], p[1]))

def power_diagram_vertices(circles):
    """
    Gera todos os vértices ponderados possíveis combinando trios de círculos.
    """
    vertices = []
    n = len(circles)
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                v = weighted_voronoi_vertex(circles[i], circles[j], circles[k])
                if v is not None:
                    vertices.append((v, (i,j,k)))

    return vertices

if __name__ == "__main__":
   fig, ax = plt.subplots(figsize=(6, 5))


   p1, p2, p3 = Point(1.0, 1.0), Point(4.0, 1.0), Point(2.5, 3.0)
   e1, e2, e3 = Edge(p1, p2), Edge(p2, p3), Edge(p3, p1)
   p4, p5, p6, p7 = Point(-1.0, -1.0), Point(6.0, -1.0), Point(6.0, 5.0), Point(-1.0, 5.0)
   e4, e5, e6, e7 = Edge(p4, p5), Edge(p5, p6), Edge(p6, p7), Edge(p7, p4)
   bounding_box = [p4, p5, p6, p7]

   triangle = Polygon([p1, p2, p3, p4, p5, p6, p7], [e1, e2, e3, e4, e5, e6, e7], bounding_box)
   # triangle = Polygon([p1, p2, p3, p4, p5, p6, p7], [e1, e2, e3], bounding_box)
   # a = plt.Polygon([(-1.0,-1.0), (6.0,-1.0), (6.0,5.0),(-1.0,5.0)])
   # ax.add_patch(a)

   triangle.generateVertexCircles()
   
   triangle.generateEdgeSubdivisions()

   triangle.generateEdgeCircles()

   triangle.splitCrowdedEdges()

   triangle.markCrowdedEdges()

   circles = triangle.getCircles()
   
   # points = [c.center for c in circles]
   # vertices = voronoi_vertices_from_delaunay(points)
   # for v, simplex in vertices:
   #    v.plot(ax, color='green')

   vertexes = power_diagram_vertices(circles)
   voronoi_circles = []
   for v, simplex in vertexes:
      min_dist = float('inf')
      validPoint = True
      for circle in circles:
         if circle.pointIsInside(v):
            validPoint = False
         elif triangle.pointInBoundingBox(v) == False:
            validPoint = False
            break
         else:
            dist = circle.center.distanceToPoint(v) - circle.radius
            if dist < min_dist:
               min_dist = dist
         
      if validPoint:
         voronoi_circles.append(Circle(v, circles[simplex[0]].distanceToPoint(v)))
     

   
   for c in voronoi_circles:
     c.center.plot(ax, color='purple')

   circles = triangle.getVertexCircles()
   for circle in circles:
      circle.plot(ax, color='red')
   
   edges = triangle.subdivisions_edges
   for edge in edges:
      if edge.crowded:
         edge.plot(ax, color='orange', linestyle='-')
      else:
         edge.plot(ax, color='blue', linestyle='-')

   vertexes = triangle.subdivisions_points + triangle.vertices
   for vertex in vertexes:
      vertex.plot(ax, color='black')

   circles = triangle.getEdgesCircles()
   for circle in circles:
      circle.plot(ax, color='green')

   # circles = voronoi_circles
   # for circle in circles:
   #    circle.plot(ax, color='purple', linestyle='--')

   circles = triangle.getCircles() 
   for circle in circles:
      for c in circles:
         if circle == c:
            continue
         if circle.circleIntersects(c):
            c.plot(ax, color='gray', linestyle='--')
         if circle.circleTouches(c):
            # c.plot(ax, color='purple', linestyle='--')
            continue


   plt.show()