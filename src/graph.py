import random

class Edge:
    def __init__(self, destination):
        self.destination=destination

class Vertex:
    def __init__(self, name, **pos):
        self.name = name
        self.color = 'red'
        self.pos = pos
        self.edges = []

class Graph:
    def __init__(self):
        self.vertexes = []

    def SetUpDebug(self):
        debugVertex1 = Vertex('debug1', x=3, y=3)
        debugVertex2 = Vertex('debug2', x=8, y=8)
        debugVertex3 = Vertex('debug3', x=3, y=8)
        debugVertex4 = Vertex('debug4', x=8, y=3)
        debugVertex1.edges = [Edge(debugVertex2), Edge(debugVertex3)]
        debugVertex2.edges = [Edge(debugVertex4)]
        self.vertexes = [debugVertex1, debugVertex2, debugVertex3, debugVertex4]

    def Randomize(self, width, height, pxBox, probability):
        # Helper function to set up two-way edges
        
        def connectVerts(v0, v1):
            v0.edges.append(Edge(v1))
            v1.edges.append(Edge(v0))

        count = 0

        # Build a grid of verts
        grid = []
        for y in range(height):
            row = []
            for x in range(width):
                v = Vertex('v' + str(count + 1))
                row.append(v)
            grid.append(row)

        # Go through the grid randomly hooking up edges
        for y in range(height):
            for x in range(width):
                # connect down
                if y < height - 1:
                    if random.random() > probability:
                        connectVerts(grid[y][x], grid[y+1][x])
                # connect right
                if x < width - 1:
                    if random.random() > probability:
                        connectVerts(grid[y][x], grid[y][x+1])

        # Last pass, set the x and y coordinates for drawing
        boxBuffer = 0.8
        boxInner = pxBox * boxBuffer
        boxInnerOffset = (pxBox - boxInner) / 2

        for y in range(height):
            for x in range(width):
                grid[y][x].pos = {
                    'x': (x * pxBox + boxInnerOffset + random.random() * boxInner),
                    'y': (y * pxBox + boxInnerOffset + random.random() * boxInner)
                }
        
        # Finally, add everything in our grid to the vertexes in this graph
        for y in range(height):
            for x in range(width):
                self.vertexes.append(grid[y][x])

    def GetColors(self):
        return [v.color for v in self.vertexes]

    def GetPositions(self):
        return [v.pos for v in self.vertexes]
