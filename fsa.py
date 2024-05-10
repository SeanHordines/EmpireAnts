import networkx as nx
import matplotlib.pyplot as plt

class FSA:
    def __init__(self):
        # graph is a nested dictionary
        # first key is the start state
        # second key is the end state
        # value is the transition vector
        self.graph = {}
        self.initialState = None
        self.currState = None

    def addState(self, state):
        # no duplicates
        if state in self.graph.keys():
            return

        # each node is a dict of edges to other nodes
        self.graph[state] = {}

        # set the inital and curr state for the first added node
        if self.initialState is None:
            self.initialState = state
            self.currState = state

    def removeState(self, state):
        # check if present first
        if state not in self.graph.keys():
            return

        del self.graph[state]

    def addEdge(self, startState, endState, transitionVector):
        # will replace a duplicate edge with new value
        self.graph[startState][endState] = transitionVector

    def removeEdge(self, startState, endState):
        # check if present first
        if endState not in self.graph[startState].keys():
            return

        del self.graph[startState][endState]

    def reset(self):
        self.currState = self.initialState

    def getInitialState(self):
        return self.initialState

    def setInitialState(self, newState):
        # check if present first
        if newState not in self.graph.keys():
            return

        self.initialState = newState

    def getCurrState(self):
        return self.currState

    def setCurrState(self, newState):
        # check if present first
        if newState not in self.graph.keys():
            return

            self.currState = newState

    def next(self, inputVector):
        newState = self.currState
        maxDotProduct = 0

        # for each edge on the curent state
        for tempState in self.graph[self.currState].keys():
            # transition vector is the edge to the end state
            tranistionVector = self.graph[self.currState][tempState]

            # only loop over the keys shared between the input and edge
            commonKeys = set(inputVector.keys()) & set(tranistionVector.keys())
            tempDotProduct = 0
            for key in commonKeys:
                # compute the dot product of the vectors
                tempDotProduct = tempDotProduct + inputVector[key]*tranistionVector[key]

            # check for new max and update
            if tempDotProduct > maxDotProduct:
                maxDotProduct = tempDotProduct
                newState = tempState

        # transition to state with the largest dot product
        self.currState = newState

    def draw(self):
        # Create a NetworkX graph object
        G = nx.DiGraph()

        # Add nodes to the graph
        for node in self.graph.keys():
            G.add_node(node)

        # Add edges to the graph
        for start_node, end_nodes in self.graph.items():
            for end_node in end_nodes.keys():
                G.add_edge(start_node, end_node)

        # Draw the graph
        pos = nx.spring_layout(G)  # Compute the layout of the nodes
        nx.draw(G, pos, with_labels=True)  # Draw the nodes and edges

        # Display the graph
        plt.axis('off')
        plt.show()
