from geometry import *

class Event:
    def __init__(self, collision:Point, time, eventType, vertexA, vertexB = None, opositeEdge = None):
        self.collision = collision
        self.time = time
        self.eventType = eventType
        self.vertexA = vertexA
        self.vertexB = vertexB
        self.opositeEdge = opositeEdge

    def isValid(self):
        if not self.vertexA.isAlive:
            return False
        if self.eventType == 'edge' and not self.vertexB.isAlive:
            return False
        return True
    
    def isSimultaneous(eventA, eventB, eps=1e-6):
        if (abs(eventA.time - eventB.time) < eps):
            if eventA.eventType == 'edge' and eventB.eventType == 'edge':
                return True 
        return False
    
    def __lt__(eventA, eventB):
        return eventA.time < eventB.time
    
    def __repr__(self):
        return f"Event type({self.eventType}), collision({self.collision}), time({self.time}) \n vertexA({self.vertexA.point}),\n vertexB({self.vertexB.point if self.vertexB else None})"