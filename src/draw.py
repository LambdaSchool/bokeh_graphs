import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval, LabelSet, Label, ColumnDataSource

from graph import Graph, Edge, Vertex

debug_graph = Graph()
debug_graph.Randomize(5, 4, 2, 0.6)
debug_graph.GetConnectedComponents()

N = len(debug_graph.vertexes)
node_indices = list(range(N))

plot = figure(title='Graph Layout Demonstration', x_range=(0,10), y_range=(0,10),
              tools='', toolbar_location=None)

graphRenderer = GraphRenderer()

graphRenderer.node_renderer.data_source.add(node_indices, 'index')
graphRenderer.node_renderer.data_source.add(debug_graph.GetColors(), 'color')
# TODO: change to circle
graphRenderer.node_renderer.glyph = Oval(height=0.5, width=0.5, fill_color='color')

startIndices = []
endIndices = []

for startIndex, vertex in enumerate(debug_graph.vertexes):
    for e in vertex.edges:
        startIndices.append(startIndex)
        endIndices.append(debug_graph.vertexes.index(e.destination))

graphRenderer.edge_renderer.data_source.data = dict(
    start=startIndices,
    end=endIndices)

x = [v.pos['x'] for v in debug_graph.vertexes]
y = [v.pos['y'] for v in debug_graph.vertexes]

graph_layout = dict(zip(node_indices, zip(x, y)))
graphRenderer.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

plot.renderers.append(graphRenderer)

# test = type(debug_graph.GetPositions()[0])

# print(test)

# add the labels
labelSource = ColumnDataSource(data=dict(
                                        x=[pos['x'] for pos in debug_graph.GetPositions()],
                                        y=[pos['y'] for pos in debug_graph.GetPositions()],
                                        names=debug_graph.GetNames()))

# TODO:  Label styles
labels = LabelSet(x='x', y='y', text='names', level='glyph',
            x_offset=-6, y_offset=-8, source=labelSource, render_mode='canvas')

plot.add_layout(labels)

output_file('../graph.html')
show(plot)