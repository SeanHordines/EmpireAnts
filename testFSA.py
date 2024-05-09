import finiteStateAutomata

behavior = finiteStateAutomata.FSA()

behavior.addState('IDLE')
behavior.addState('MOVING')
behavior.addState('COLLECTING')

behavior.addEdge('IDLE', 'MOVING', 'A')

behavior.addEdge('MOVING', 'IDLE', 'B')
behavior.addEdge('MOVING', 'COLLECTING', 'C')

behavior.addEdge('COLLECTING', 'IDLE', 'B')
behavior.addEdge('COLLECTING', 'MOVING', 'A')

behavior.draw()
