import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor

class FSA:
    def __init__(self):
        self.graph = nx.DiGraph()

    def addState(self, state):
        self.graph.add_node(state)

    def removeState(self, state):
        self.graph.remove_node(state)

    def addEdge(self, startState, endState, value):
        self.graph.add_edge(startState, endState, label=value)

    def remove_edge(self, startState, endState):
        self.graph.remove_edge(startState, endState)

    def draw(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', font_size=8)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=nx.get_edge_attributes(self.graph, 'label'), font_size=8)
        plt.axis('off')
        plt.show()
