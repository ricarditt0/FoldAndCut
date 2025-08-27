import geometry
import math
import unittest

class testPointMethods(unittest.TestCase):
    
    def test_distance_to_point(self):
        # Create points
        p1 = geometry.Point(1.0, 2.0)
        p2 = geometry.Point(4.0, 6.0)

        # Assert the expected distance
        self.assertEqual(p1.distance_to_point(p2), 5.0)
        self.assertEqual(p2.distance_to_point(p1), 5.0)
        self.assertEqual(p1.distance_to_point(p1), 0.0)


class testEdgeMethods(unittest.TestCase):
    def test_edge_distance_to_point(self):
        # Create points and edge
        start = geometry.Point(1.0, 1.0)
        end = geometry.Point(4.0, 4.0)
        edge = geometry.edge(start, end)
        p1 = geometry.Point(2.0, 3.0)
        p2 = geometry.Point(3.0, 3.0)
        p3 = geometry.Point(4.0, 5.0)
        p4 = geometry.Point(1.0, 0.0)

        # Calculate distances
        distance1 = edge.distance_to_point(p1)
        distance2 = edge.distance_to_point(p2)
        distance3 = edge.distance_to_point(p3)
        distance4 = edge.distance_to_point(p4)
        
        # Assert the expected distance
        self.assertEqual(distance1, 0.7071067811865476)
        self.assertEqual(distance2, 0)
        self.assertEqual(distance3, 1)
        self.assertEqual(distance4, 1)


class testCircleMethods(unittest.TestCase):
    def test_circle_intersects(self):
        # Create circles
        c1 = geometry.Circle(geometry.Point(2, 7), 1.0)
        c2 = geometry.Circle(geometry.Point(2, 3), 1.0)
        c3 = geometry.Circle(geometry.Point(2, 1), 1.0)
        c4 = geometry.Circle(geometry.Point(7, 4), 1.0)
        c5 = geometry.Circle(geometry.Point(8, 3), 3.0)
        c6 = geometry.Circle(geometry.Point(14, 6), 2.0)
        c7 = geometry.Circle(geometry.Point(14, 4), 1.0)

        # Assert intersection
        self.assertFalse(c2.circle_intersects(c3)) # No intersection
        self.assertTrue(c4.circle_intersects(c5))  # Intersection
        self.assertTrue(c6.circle_intersects(c7)) # Intersection
        self.assertFalse(c1.circle_intersects(c2))  # No intersection
        self.assertFalse(c1.circle_intersects(c4))  # No intersection
        self.assertFalse(c1.circle_intersects(c6)) # No intersection


class testPolygonMethods(unittest.TestCase):
    def test_polygon_edges(self):
        # Create points and polygon
        p1 = geometry.Point(1.0, 1.0)
        p2 = geometry.Point(4.0, 1.0)
        p3 = geometry.Point(2.5, 3.0)
        triangle = geometry.Polygon([p1, p2, p3])

        # Get edges
        edges = triangle.edges

        # Assert the expected edges
        self.assertEqual((edges[0].start, edges[0].end), (p1, p2))
        self.assertEqual((edges[1].start, edges[1].end), (p2, p3))
        self.assertEqual((edges[2].start, edges[2].end), (p3, p1))


if __name__ == "__main__":

    unittest.main()