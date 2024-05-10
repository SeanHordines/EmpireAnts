class FSA:
    def __init__(self):
        # graph is a nested dictionary
        # first key is the start state
        # second key is the end state
        # value is the transition vector
        self.graph = {}
        self.initialState = None
        self.currState = None

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

    def addState(self, state):
        # each node is a dict of edges to other nodes
        self.graph[state] = {}

        # set the inital and curr state for the first added node
        if self.initialState is None:
            self.initialState = state
            self.currState = state

    def removeState(self, state):
        del self.graph[state]

    def addEdge(self, startState, endState, transitionVector):
        self.graph[startState][endState] = transitionVector

    def removeEdge(self, startState, endState):
        del self.graph[startState][endState]

    def reset(self):
        self.currState = self.initialState
