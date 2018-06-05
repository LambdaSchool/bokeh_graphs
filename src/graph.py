import random

class Edge:
    def __init__(self, destination):
        self.destination=destination

class Vertex:
    def __init__(self, name, **pos):
        self.name = name
        self.color = 'white'
        self.pos = pos
        self.edges = []

class Graph:
    def __init__(self):
        self.vertexes = []

    def set_up_debug(self):
        debut_vertex_1 = Vertex('debug1', x=3, y=3)
        debug_vertex_2 = Vertex('debug2', x=8, y=8)
        debug_vertex_3 = Vertex('debug3', x=3, y=8)
        debug_vertex_4 = Vertex('debug4', x=8, y=3)
        debut_vertex_1.edges = [Edge(debug_vertex_2), Edge(debug_vertex_3)]
        debug_vertex_2.edges = [Edge(debug_vertex_4)]
        self.vertexes = [debut_vertex_1, debug_vertex_2, debug_vertex_3, debug_vertex_4]

    def randomize(self, width, height, px_box, probability):
        # Helper function to set up two-way edges
        
        def connect_verts(v0, v1):
            v0.edges.append(Edge(v1))
            v1.edges.append(Edge(v0))

        count = 0

        # Build a grid of verts
        grid = []
        for y in range(height):
            row = []
            for x in range(width):
                v = Vertex('v' + str(count + 1))
                count += 1
                row.append(v)
            grid.append(row)

        # Go through the grid randomly hooking up edges
        for y in range(height):
            for x in range(width):
                # connect down
                if y < height - 1:
                    if random.random() > probability:
                        connect_verts(grid[y][x], grid[y+1][x])
                # connect right
                if x < width - 1:
                    if random.random() > probability:
                        connect_verts(grid[y][x], grid[y][x+1])

        # Last pass, set the x and y coordinates for drawing
        box_buffer = 0.8
        box_inner = px_box * box_buffer
        box_inner_offset = (px_box - box_inner) / 2

        for y in range(height):
            for x in range(width):
                grid[y][x].pos = {
                    'x': (x * px_box + box_inner_offset + random.random() * box_inner),
                    'y': (y * px_box + box_inner_offset + random.random() * box_inner)
                }
        
        # Finally, add everything in our grid to the vertexes in this graph
        for y in range(height):
            for x in range(width):
                self.vertexes.append(grid[y][x])

    def breadth_first_search(self, start, reset=True):
        color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        
        start.color = color
        queue = []
        queue.append(start)

        while len(queue) > 0:
            vertex = queue[0]

            for edge in vertex.edges:
                dest = edge.destination
                if dest.color == 'white':
                    dest.color = color
                    queue.append(dest)

            queue.pop(0)

    def get_connected_components(self):
        for vertex in self.vertexes:
            if vertex.color == 'white':
                self.breadth_first_search(vertex)

    def get_colors(self):
        return [v.color for v in self.vertexes]

    def get_positions(self):
        return [v.pos for v in self.vertexes]

    def get_names(self):
        return [v.name for v in self.vertexes]
