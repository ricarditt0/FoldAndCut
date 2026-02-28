from Lav import *
from geometry import *
from Event import *
from Skeleton import *
import heapq
import json

def load_json(filepath,polygon):
    points = []
    holes = []
    with open (filepath, 'r') as f:
        data = json.load(f)
    for name, info in data.items():
        if name == polygon:
            for p in info["points"]:
                points.append(Point(p[0], p[1])) 
    return points

def build_polygon(points):
    n = len(points)
    
    old_vertex = Vertex(points[0])
    init_vertex = old_vertex
    init_vertex.first = True

    for i in range(1, n):
        new_vertex = Vertex(points[i])

        old_vertex.next = new_vertex
        new_vertex.prev = old_vertex

        old_vertex = new_vertex

    old_vertex.next = init_vertex
    init_vertex.prev = old_vertex

    return init_vertex


class StraightSkeleton:
    def __init__(self, polygon_points):
        self.polygon_points = polygon_points
        self.slav = Slav()
        self.eventQueue = []
        self.skeletonGraph = graph()
        self.buildFirstLAV(polygon_points)
        self.inicializeEventQueue()

    def findEdgeEvent(vertexA, vertexB):
        if vertexB is not None:
  
            if vertexA == vertexB:
                return None

            vertexA.bisecting()
            vertexB.bisecting()
            rayA = vertexA.rayDirection
            rayB = vertexB.rayDirection

            intersection = rayA.intersect(rayB)
            if intersection is None:
                return None

            point, t1, t2 = intersection

            return Event(point, t1, 'edge', vertexA, vertexB)
        else:
            raise ValueError("Vertex does not have a next vertex.")

    def findSplitEvent(self, vertex):
        # Implement the logic to find the split event for the given vertex
        pass

    def handleEdgeEvent(self, event):
        vertexA = event.vertexA
        vertexB = event.vertexB
        lav = vertexA.lav

        # Mark vertices as processed
        vertexA.processed = True
        vertexB.processed = True

        # Create a new vertex at the collision point
        newVertex = Vertex(event.collison)
        newVertex.processed = True

        # Update the linked list to include the new vertex
        lav.insert_vertex_between(vertexA.prev, vertexB.next, newVertex)

        # Remove the old vertices from the linked list
        newVertex.lav = lav
        lav.remove_vertex(vertexA)
        lav.remove_vertex(vertexB)

        # Compute the bisecting ray for the new vertex
        newVertex.bisecting()
        newVertex.prev.bisecting()    
        newVertex.next.bisecting()

        # Schedule new events for the affected vertices
        edgeEventA = StraightSkeleton.findEdgeEvent(newVertex.prev, newVertex)
        edgeEventB = StraightSkeleton.findEdgeEvent(newVertex, newVertex.next)

        if edgeEventA is not None:
            heapq.heappush(self.eventQueue, edgeEventA)
        if edgeEventB is not None:
            heapq.heappush(self.eventQueue, edgeEventB)

        # Update the skeleton graph
        self.skeletonGraph.add_vertice(event.collison)
        self.skeletonGraph.add_vertice(vertexA.point)
        self.skeletonGraph.add_vertice(vertexB.point)
        self.skeletonGraph.add_edge(Edge(vertexA.point, event.collison))
        self.skeletonGraph.add_edge(Edge(vertexB.point, event.collison))

        return newVertex
        

    def handleSplitEvent(self, event):
        # Implement the logic to handle split events
        pass
    
    def find_unprocessed_vertex(self):
        for lav in self.slav.lavs:
            vertex = lav.head
            while True:
                if not vertex.processed and vertex.isAlive:
                    return vertex
                vertex = vertex.next
                if vertex.first:
                    break
        return None

    def buildFirstLAV(self, polygon_points):
        init_vertex = build_polygon(polygon_points)
        lav = Lav(init_vertex)
        self.slav.addLav(lav)
        vertex = lav.head
        while True:
            vertex = vertex.next
            vertex.bisecting()
            vertex.lav = lav
            lav.count += 1
            if vertex.first:
                break


    def inicializeEventQueue(self):
        for lav in self.slav.lavs:
            vertex = lav.head
            while True:
                event = StraightSkeleton.findEdgeEvent(vertex, vertex.next)
                if event is not None:
                    heapq.heappush(self.eventQueue, event)
                vertex = vertex.next
                if vertex.first:
                    break
    
    def run(self):
        while self.eventQueue:
            event = heapq.heappop(self.eventQueue)
            if not event.isValid():
                continue


            if event.eventType == 'edge':
                self.handleEdgeEvent(event)
                print(f"Processed edge event: {event}")

            elif event.eventType == 'split':
                self.handleSplitEvent(event)

        # leftover_vertex = self.find_unprocessed_vertex()
        # while leftover_vertex is not None:
        #     self.skeletonGraph.add_vertice(leftover_vertex.point)
        #     self.skeletonGraph.add_edge(Edge(leftover_vertex.point, leftover_vertex.prev.point))
        #     self.skeletonGraph.add_edge(Edge(leftover_vertex.point, leftover_vertex.next.point))
        #     leftover_vertex.processed = True
        #     leftover_vertex = self.find_unprocessed_vertex()


if __name__ == "__main__":
    fig1, ax = plt.subplots(figsize=(6, 5))
    fig2, b = plt.subplots(figsize=(6, 5))
    fig3, a = plt.subplots(figsize=(6, 5))

    points = load_json('polygons.json','triangle')

    
    skeleton = StraightSkeleton(points)
    skeleton.slav.lavs[0].draw(b)
    for event in skeleton.eventQueue:
        print(event)

    skeleton.run()
    skeleton.skeletonGraph.draw(a)
    skeleton.slav.lavs[0].draw(ax)
    plt.title("Straight Skeleton")
    plt.show()