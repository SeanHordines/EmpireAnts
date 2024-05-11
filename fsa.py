import networkx as nx
import matplotlib.pyplot as plt
import json
from typing import Dict, Tuple, Union

def Node(name, func = None, edges = None):
    if func is None:
        func = ""
    if edges is None:
        edges = {}
    return {'name': name, 'func': func, 'edges': edges}

class FSA:
    def __init__(self, name: str = None, filepath: str = None):
        # graph is a nested dictionary
        # first key is the start state
        # second key is the end state
        # value is the transition vector
        self.name = name
        self.initialState = None
        self.currState = None
        self.nodes = {}

        if filepath:
            loadJSON(self, filepath)

    def addState(self, state: Node) -> None:
        # no duplicates
        if state['name'] in self.nodes:
            return

        # each node is a dict of edges to other nodes
        self.nodes[state['name']] = state

        # set the inital and curr state for the first added node
        if self.initialState is None:
            self.initialState = state['name']
            self.currState = state['name']

    def removeState(self, stateName: str) -> None:
        # check if present first
        if stateName not in self.nodes:
            return

        # delete the state from the top level dict
        del self.nodes[stateName]

        # delete all references to the deleted state
        for iterStateName in self.nodes:
            if stateName in self.nodes[iterStateName]['edges']:
                del self.nodes[iterStateName]['edges'][stateName]

    def addEdge(self, startStateName: str, endStateName: str, transitionVector: Dict[Node, Union[int, float]]) -> None:
        # check if adding states is necessary
        if startStateName not in self.nodes:
            self.addState(Node(startStateName))
        if endStateName not in self.nodes:
            self.addState(Node(endStateName))

        # will replace a duplicate edge with new value
        self.nodes[startStateName]['edges'][endStateName] = transitionVector

    def removeEdge(self, startStateName: str, endStateName: str) -> None:
        # check if present first
        if startStateName not in self.nodes:
            return
        if endStateName not in self.nodes:
            return
        if endStateName not in self.nodes[startStateName]['edges']:
            return

        del self.nodes[startStateName]['edges'][endStateName]

    def merge(self, other: str) -> None:
        for startStateName, startState in other.nodes.items():
            if startStateName not in self.nodes:
                self.nodes[startStateName] = startState

            for endStateName, transitionVector in startState['edges'].items():
                if endStateName not in self.nodes[startStateName]['edges']:
                    self.nodes[startStateName]['edges'][endStateName] = transitionVector

    def reset(self):
        self.currState = self.initialState

    def getInitialState(self) -> str:
        return self.initialState

    def setInitialState(self, newStateName: str) -> None:
        # check if present first
        if newStateName not in self.nodes:
            return

        self.initialState = newStateName

    def getCurrState(self) -> str:
        return self.currState

    def setCurrState(self, newStateName: str) -> None:
        # check if present first
        if newStateName not in self.nodes:
            return

            self.currState = newStateName

    def next(self, inputVector: Dict[str, Union[int, float]]) -> str:
        newState = self.currState
        maxDotProduct = 0

        # for each edge on the curent state
        for iterStateName, tranistionVector in self.nodes[self.currState]['edges'].items():
            # transition vector is the edge to the end state

            # only loop over the keys shared between the input and edge
            commonKeys = set(inputVector.keys()) & set(tranistionVector.keys())
            iterDotProduct = 0
            for key in commonKeys:
                # compute the dot product of the vectors
                iterDotProduct += inputVector[key]*tranistionVector[key]

            # check for new max and update
            if iterDotProduct > maxDotProduct:
                maxDotProduct = iterDotProduct
                newState = iterStateName

        # transition to state with the largest dot product
        self.currState = newState
        return self.currState

def draw(fsa: FSA) -> None:
    # Create a NetworkX graph object
    G = nx.DiGraph()

    # Add nodes to the graph
    for stateName in fsa.nodes.keys():
        G.add_node(stateName)

    # Add edges to the graph
    for startStateName, startState in fsa.nodes.items():
        for endStateName in startState['edges'].keys():
            G.add_edge(startStateName, endStateName)

    # Draw the graph
    pos = nx.spring_layout(G)  # Compute the layout of the nodes
    nx.draw(G, pos, with_labels=True)  # Draw the nodes and edges

    # Display the graph
    plt.axis('off')
    plt.show()

def saveJSON(fsa: FSA, filepath: str) -> None:
    with open(filepath, "w") as file:
        data = {"name": fsa.name,
            "initial": fsa.initialState,
            "current": fsa.currState,
            "nodes": fsa.nodes}
        json.dump(data, file, indent=4)

def loadJSON(fsa: FSA, filepath: str) -> FSA:
    with open(filepath, "r") as file:
        data = json.load(file)
        fsa.name = data["name"]
        fsa.initialState = data["initial"]
        fsa.currState = data["current"]
        fsa.nodes = data["nodes"]
        return fsa
