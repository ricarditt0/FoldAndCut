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

            distance = point.distanceToSegment(vertexA.point, vertexB.point)

            return Event(point, distance, 'edge', vertexA, vertexB)
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
        newVertex = Vertex(event.collision)

        # Update the linked list to include the new vertex
        lav.insert_vertex_between(vertexA, vertexB, newVertex)

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
        self.skeletonGraph.add_vertice(event.collision)
        self.skeletonGraph.add_vertice(vertexA.point)
        self.skeletonGraph.add_vertice(vertexB.point)
        self.skeletonGraph.add_edge(Edge(vertexA.point, event.collision))
        self.skeletonGraph.add_edge(Edge(vertexB.point, event.collision))

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
    
    def find_simultaneous_events(self, cluster_events):
        for event in self.eventQueue:
            if event.isSimultaneous(cluster_events[0]):
                if event.isValid():
                    cluster_events.append(event)
                    self.eventQueue.remove(event)
            else:
                break

    def cluster_by_collision(self, cluster_events):
        clusters = []
        for event in cluster_events:
            added = False
            for cluster in clusters:
                if cluster[0] is None:
                    cluster.append(event)
                    added = True
                    break
                elif Point.same_point(cluster[0].collision, event.collision):
                    cluster.append(event)
                    added = True
                    break
            if not added:
                clusters.append([event])
        return clusters
        

    def handle_cluster(self, cluster_events):
        clusters = self.cluster_by_collision(cluster_events)

        involved_vertices = set()
        for cluster in clusters:

            #add the collision point as a vertice in the skeleton graph
            collision_point = cluster[0].collision
            lav = cluster[0].vertexA.lav
            newVertex = Vertex(collision_point)
            newVertex.lav = lav
            self.skeletonGraph.add_vertice(collision_point)

            if lav.head.prev.prev == lav.head.next:
                # This is a special case where the new vertex creates a peak of roof
                vertexA = lav.head
                vertexB = lav.head.next
                vertexC = lav.head.prev

                vertexA.processed = True
                vertexB.processed = True
                vertexC.processed = True

                lav.remove_vertex(vertexA)
                lav.remove_vertex(vertexB)
                lav.remove_vertex(vertexC)

                self.slav.removeLav(lav)

                 # Update the skeleton graph
                self.skeletonGraph.add_vertice(vertexA.point)
                self.skeletonGraph.add_vertice(vertexB.point)
                self.skeletonGraph.add_vertice(vertexC.point)
                self.skeletonGraph.add_edge(Edge(vertexC.point, collision_point))
                self.skeletonGraph.add_edge(Edge(vertexA.point, collision_point))
                self.skeletonGraph.add_edge(Edge(vertexB.point, collision_point))
                print(f"Processed peak of roof event: {cluster[0]}")
                continue

            for event in cluster:
                involved_vertices.add(event.vertexA)
                event.vertexA.next = newVertex
                
                if event.vertexB is not None:
                    involved_vertices.add(event.vertexB)
                    event.vertexB.prev = newVertex

            for vertex in involved_vertices:

                if vertex.next != newVertex:
                    newVertex.next = vertex.next
                    vertex.next.prev = newVertex
                elif vertex.prev != newVertex:
                    newVertex.prev = vertex.prev
                    vertex.prev.next = newVertex

                vertex.processed = True
                self.skeletonGraph.add_vertice(vertex.point)
                self.skeletonGraph.add_edge(Edge(vertex.point, newVertex.point))
                
                # Mark the old vertices as processed and remove them from the linked list
                vertex.processed = True
                vertex.isAlive = False
                vertex.prev = None
                vertex.next = None
                vertex.lav.count -= 1
                vertex.lav = None

            if newVertex.lav.count > 1:
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
            else:
                self.slav.removeLav(lav)

            
            #prepare for the next cluster
            involved_vertices.clear()

        return newVertex

                
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

            cluster_events = [event]
            if self.eventQueue:
                if self.eventQueue[0].isSimultaneous(event):
                    self.find_simultaneous_events(cluster_events)
                else:
                    cluster_events.remove(event)

            if cluster_events:
                self.handle_cluster(cluster_events)

            elif event.eventType == 'edge':
                self.handleEdgeEvent(event)
                print(f"Processed edge event: {event}")

            elif event.eventType == 'split':
                self.handleSplitEvent(event)

        leftover_vertex = self.find_unprocessed_vertex()
        while leftover_vertex is not None:
            self.skeletonGraph.add_vertice(leftover_vertex.point)
            self.skeletonGraph.add_edge(Edge(leftover_vertex.point, leftover_vertex.prev.point))
            self.skeletonGraph.add_edge(Edge(leftover_vertex.point, leftover_vertex.next.point))
            leftover_vertex.processed = True
            leftover_vertex = self.find_unprocessed_vertex()


if __name__ == "__main__":
    fig1, ax = plt.subplots(figsize=(6, 5))
    fig2, b = plt.subplots(figsize=(6, 5))
    fig3, a = plt.subplots(figsize=(6, 5))

    points = load_json('polygons.json','rectangle')


    
    skeleton = StraightSkeleton(points)
    skeleton.slav.lavs[0].draw(b)

    
    skeleton.run()
    skeleton.skeletonGraph.draw(a)
    
    plt.title("Straight Skeleton")
    plt.show()