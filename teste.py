from geometry import *
import math
import unittest
from foldAndCut import *

class testPointMethods(unittest.TestCase):
    
    def test_distance_to_point(self):
        # Create points
        p1 = Point(1.0, 2.0)
        p2 = Point(4.0, 6.0)

        # Assert the expected distance
        self.assertEqual(p1.distanceToPoint(p2), 5.0)
        self.assertEqual(p2.distanceToPoint(p1), 5.0)
        self.assertEqual(p1.distanceToPoint(p1), 0.0)


class testEdgeMethods(unittest.TestCase):
    def test_edge_distance_to_point(self):
        # Create points and edge
        start = Point(1.0, 1.0)
        end = Point(4.0, 4.0)
        edge = Edge(start, end)
        p1 = Point(2.0, 3.0)
        p2 = Point(3.0, 3.0)
        p3 = Point(4.0, 5.0)
        p4 = Point(1.0, 0.0)

        # Calculate distances
        distance1 = edge.distanceToPoint(p1)
        distance2 = edge.distanceToPoint(p2)
        distance3 = edge.distanceToPoint(p3)
        distance4 = edge.distanceToPoint(p4)
        
        # Assert the expected distance
        self.assertEqual(distance1, 0.7071067811865476)
        self.assertEqual(distance2, 0)
        self.assertEqual(distance3, 1)
        self.assertEqual(distance4, 1)

    def test_is_incident(self):
        # Create points and edge
        start = Point(1.0, 1.0)
        end = Point(4.0, 4.0)
        edge = Edge(start, end)
        p1 = Point(2.0, 1.0)
        p2 = Point(4.0, 4.0)
        p3 = Point(3.0, 3.0)
        p4 = Point(1.0, 1.0)

        # Assert incident points
        self.assertTrue(edge.isIncident(start))
        self.assertTrue(edge.isIncident(end))
        self.assertFalse(edge.isIncident(p1))
        self.assertTrue(edge.isIncident(p2))
        self.assertFalse(edge.isIncident(p3))
        self.assertTrue(edge.isIncident(p4))


class testCircleMethods(unittest.TestCase):
    def test_circle_intersects(self):
        # Create circles
        c1 = Circle(Point(2, 7), 1.0)
        c2 = Circle(Point(2, 3), 1.0)
        c3 = Circle(Point(2, 1), 1.0)
        c4 = Circle(Point(7, 4), 1.0)
        c5 = Circle(Point(8, 3), 3.0)
        c6 = Circle(Point(14, 6), 2.0)
        c7 = Circle(Point(14, 4), 1.0)

        # Assert intersection
        self.assertFalse(c2.circleIntersects(c3)) # No intersection
        self.assertTrue(c4.circleIntersects(c5))  # Intersection
        self.assertTrue(c6.circleIntersects(c7)) # Intersection
        self.assertFalse(c1.circleIntersects(c2))  # No intersection
        self.assertFalse(c1.circleIntersects(c4))  # No intersection
        self.assertFalse(c1.circleIntersects(c6)) # No intersection


class testPolygonMethods(unittest.TestCase):
    def test_polygon_edges(self):
        # Create points and polygon
        p1 = Point(1.0, 1.0)
        p2 = Point(4.0, 1.0)
        p3 = Point(2.5, 3.0)
        triangle = Polygon([p1, p2, p3])

        # Get edges
        edges = triangle.edges

        # Assert the expected edges
        self.assertEqual(edges[0],Edge(p1, p2))
        self.assertEqual(edges[1],Edge(p2, p3))
        self.assertEqual(edges[2],Edge(p3, p1))
        self.assertEqual(edges[0],Edge(p2, p1))
        self.assertEqual(edges[1],Edge(p3, p2))
        self.assertEqual(edges[2],Edge(p1, p3))


class testFoldAndCutMethods(unittest.TestCase):
    def test_generate_vertex_circles(self):
        # Create triangle and rectangle
        p1, p2, p3 = Point(1.0, 1.0), Point(4.0, 1.0), Point(2.5, 3.0)
        triangle = Polygon([p1, p2, p3])
        p4, p5, p6, p7 = Point(0.0, 0.0), Point(5.0, 0.0), Point(5.0, 4.0), Point(0.0, 4.0)
        rectangle = Polygon([p4, p5, p6, p7])

        # Generate circles
        circles = generateVertexCircles(triangle, rectangle)
        expected_radius = [0.5, 0.5, 0.5, 0.7, 0.7, 1.3, 1.3]
        vertex = triangle.vertices + rectangle.vertices

        # Assert the expected circles
        for c in range(len(circles)):
            circle = circles.pop(0)
            expec_rad = expected_radius.pop(0)
            self.assertAlmostEqual(circle.radius, expec_rad, places=1, msg='failed {c}')
            self.assertEqual(circle.center, vertex[c], msg='failed center {c}')



if __name__ == "__main__":

    unittest.main()