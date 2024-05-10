import fsa

filepath1 = "D:/Sean/programmingshit/EmpireAnts/sampleFSA1.json"
filepath2 = "D:/Sean/programmingshit/EmpireAnts/sampleFSA2.json"

behavior = fsa.FSA()

behavior.addState('IDLE')
behavior.addState('MOVING')

behavior.addEdge('IDLE', 'MOVING', {'paramB': 1})
behavior.addEdge('MOVING', 'IDLE', {'paramA': 1})

fsa.saveJSON(behavior, filepath1)

behavior.next({'paramA': 1, 'paramB': 0})
behavior.next({'paramA': 0, 'paramB': 1})
behavior.next({'paramA': 0, 'paramB': 1})
behavior.next({'paramA': 1, 'paramB': 0})
behavior.next({'paramA': 0, 'paramB': 1})

behavior.setInitialState('MOVING')
behavior.reset()
print(behavior.getCurrState())

behavior = fsa.loadJSON(filepath1)
print(behavior.getCurrState())

# fsa.draw(behavior)

second = fsa.FSA()
second.addState('GATHERING')
second.addState('PRODUCING')

second.addEdge('GATHERING', 'PRODUCING', {'paramC': 1})
second.addEdge('PRODUCING', 'GATHERING', {'paramD': 1})

fsa.saveJSON(second, filepath2)

behavior.merge(second)

behavior.addEdge('IDLE', 'GATHERING', {'paramD': 1})
behavior.addEdge('PRODUCING', 'MOVING', {'paramC': 1})

fsa.draw(behavior)
