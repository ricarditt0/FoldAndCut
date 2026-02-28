from geometry import *
import matplotlib.pyplot as plt

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