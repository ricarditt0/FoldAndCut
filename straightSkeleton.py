import matplotlib.pyplot as plt
import json
import heapq

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

class Edge:
    def __init__(self, ini:Point, end:Point):
        self.ini = ini
        self.end = end
        self.isEdge = True
    
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

class graph:
    def __init__(self):
        self.edges = []
        self.vertices = set()

    def add_vertice(self, vertice:Point):
        self.vertices.add(vertice)
    
    def add_edge(self, edge:Edge):
        self.edges.append(edge)

    def draw(self, ax, colorP='blue',colorE='red'):
        for edge in self.edges:
            edge.draw(ax, color=colorP)
        for vertex in self.vertices:
            vertex.draw(ax, color=colorE)

class Vertex:
    def __init__(self, point:Point, inEdge:Edge, outEdge:Edge):
        self.point = point
        self.prev = None
        self.next = None
        self.outEdge = outEdge
        self.inEdge = inEdge

        self.processed = False
        self.isAlive = True
        self._isReflex = False
        self.rayDirection = None

    def isReflex(self):
        # Vetores
        v_prev = self.point - self.prev.point
        v_next = self.next.point - self.point
        
        # Cross product
        cross = v_prev.x * v_next.y - v_prev.y * v_next.x
        self._isReflex = cross < 0

        return cross < 0  # CCW polygon rule

    def __eq__(self, value):
        return self.point == value.point #pode dar problema no futuro

    def bisecting(self):
        self.isReflex()
        if self._isReflex:
            dirIn = (self.point - self.inEdge.ini).normalize()
            dirOut = (self.point - self.outEdge.end).normalize()
            bicectDir = (dirIn + dirOut).normalize()

        else:
            dirIn = (self.inEdge.ini - self.point).normalize()
            dirOut = (self.outEdge.end - self.point).normalize()
            bicectDir = (dirIn + (dirOut)).normalize()
    
        self.rayDirection =  Ray(self.point, bicectDir)
        return  bicectDir 

class Event:
    def __init__(self, collison:Point, vertexA: Vertex, vertexB:Vertex, time:float , type:str):
        self.vertexA = vertexA
        self.vertexB = vertexB
        self.collison = collison
        self.type = type
        self.time = time
        # self.merged = False
        # self.listOfMerged = {}

    def __lt__(eventA, eventB):
        return eventA.time < eventB.time

    def __repr__(self):
        return f"Event type({self.type}), collision({self.collison}), time({self.time})"
    
    def isValid(self):
        return self.vertexA.isAlive and self.vertexB.isAlive

    def findEdgeEvent(vertexA:Vertex, vertexB:Vertex):

        if vertexA == vertexB:
            return None

        rayA = vertexA.rayDirection
        rayB = vertexB.rayDirection

        intersection = rayA.intersect(rayB)
        if intersection is None:
            return None

        point, t1, t2 = intersection

        return Event(point, vertexA, vertexB, t1, 'edge')
    
    def processEdgeEvent(self , skeletonGraph:graph):
        
        vertexA = self.vertexA
        vertexB = self.vertexB
        vertexA.processed = True
        vertexB.processed = True

        # Mark vertices as not alive
        vertexA.isAlive = False
        vertexB.isAlive = False

        # Create a new vertex at the collision point
        newInEdge = Edge(vertexA.prev.point, self.collison)
        newOutEdge = Edge(self.collison, vertexB.next.point)
        newVertex = Vertex(self.collison, newInEdge, newOutEdge)
        newVertex.processed = True

        # Update the linked list to include the new vertex
        newVertex.prev = vertexA.prev
        newVertex.next = vertexB.next
        vertexA.prev.next = newVertex
        vertexB.next.prev = newVertex

        # Compute the bisecting ray for the new vertex
        newVertex.bisecting()
        newVertex.prev.bisecting()
        newVertex.next.bisecting()

        vertexA.next = None
        vertexA.prev = None
        vertexB.next = None
        vertexB.prev = None

        skeletonGraph.add_vertice(self.collison)
        skeletonGraph.add_vertice(vertexA.point)
        skeletonGraph.add_vertice(vertexB.point)
        skeletonGraph.add_edge(Edge(vertexA.point, self.collison))
        skeletonGraph.add_edge(Edge(vertexB.point, self.collison))

        return newVertex

    
    def __eq__(self,other):
        return Point.almost_equal(self.collison, other.collison) and self.vertexA == other.vertexA and self.vertexB == other.vertexB and self.type == other.type
    
    # def mergeAppend(self, other):
    #     self.listOfMerged.add(other.vertexA)
    #     self.listOfMerged.add(other.vertexB)
    #     if other.merged:
    #         self.listOfMerged.update(other.listOfMerged)

    # def findequalEvents(self, listOfEvents):
    #     for event in listOfEvents:
    #         if self == event:
    #             return event
    #     return None
    
    def draw(self, ax, color='magenta'):
        self.collison.draw(ax, color=color)
        self.vertexA.point.draw(ax, color='cyan')
        self.vertexB.point.draw(ax, color='cyan')
        self.vertexA.rayDirection.draw(ax, length=10.0, color='orange')
        self.vertexB.rayDirection.draw(ax, length=10.0, color='orange')
        

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
    edges = []
    n = len(points)
    for i in range(n):
        edge = Edge(points[i], points[(i + 1) % n])
        edges.append(edge)

    
    n = len(edges)    
    old_vertex = Vertex(edges[0].ini, edges[-1], edges[0])
    init_vertex = old_vertex
    init_vertex.first = True

    for i in range(1, n):
        new_vertex = Vertex(edges[i].ini, edges[i-1], edges[i])

        old_vertex.next = new_vertex
        new_vertex.prev = old_vertex

        old_vertex = new_vertex

    old_vertex.next = init_vertex
    init_vertex.prev = old_vertex

    return init_vertex , edges
            
        
    


if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(6, 5))

    points = load_json('polygons.json','hexagon_convex')
    polygon,edges = build_polygon(points)

    #Set of List of Active Vertices
    Slav = []
    endOfList = polygon.prev
    originalListOfVertices = []

    while True:
        originalListOfVertices.append(polygon)
        polygon.bisecting()
        # polygon.rayDirection.draw(ax, length=10.0, color='green')
        polygon.point.draw(ax, color='blue')
        # polygon.outEdge.draw(ax, color='red')
        
        if polygon == endOfList:
            break
        polygon = polygon.next

    plt.show()

    listOfEvents = []
    Slav.append(polygon)
    for lav in Slav:
        vertex = lav
        endOfList = vertex.prev
        while True:
            if vertex._isReflex:
                continue
            else:
                event = Event.findEdgeEvent(vertex, vertex.next)

            if event is not None:
                heapq.heappush(listOfEvents, event)
            
            if vertex == endOfList:
                break

            vertex = vertex.next

    skeletonGraph = graph()

    newVertex = None

    while listOfEvents:
        currentEvent = heapq.heappop(listOfEvents)
        if not currentEvent.isValid():
            continue
        else:
            if currentEvent.type == 'edge':
                newVertex = currentEvent.processEdgeEvent(skeletonGraph)
                # Add new events involving the new vertex
                eventA = Event.findEdgeEvent(newVertex.prev, newVertex)
                eventB = Event.findEdgeEvent(newVertex, newVertex.next)
                if eventA is not None:
                    heapq.heappush(listOfEvents, eventA)
                if eventB is not None:
                    heapq.heappush(listOfEvents, eventB)
            
    for v in originalListOfVertices:
        if v.processed == False:
            skeletonGraph.add_vertice(v.point)
            skeletonGraph.add_edge(Edge(v.point, v.next.point))
            skeletonGraph.add_edge(Edge(v.point, v.prev.point))

    skeletonGraph.draw(ax)
    print(skeletonGraph.vertices)
   
    
    plt.show()