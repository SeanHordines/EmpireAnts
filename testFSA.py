import fsa

filepath1 = "D:/Sean/programmingshit/EmpireAnts/sampleFSA1.json"
filepath2 = "D:/Sean/programmingshit/EmpireAnts/sampleFSA2.json"


first = fsa.FSA("test1")
first.addState(fsa.Node('IDLE'))
first.addState(fsa.Node('MOVING', 'move'))
first.addEdge('IDLE', 'MOVING', {'paramA': 1})
first.addEdge('MOVING', 'IDLE', {'paramB': 1})
# fsa.draw(first)
fsa.saveJSON(first, filepath1)

second = fsa.FSA("test2")
second.addState(fsa.Node('GATHERING'))
second.addState(fsa.Node('PRODUCING'))
second.addEdge('GATHERING', 'PRODUCING', {'paramC': 1})
second.addEdge('PRODUCING', 'GATHERING', {'paramD': 1})
# fsa.draw(second)
fsa.saveJSON(second, filepath2)

third = fsa.FSA("test3", filepath1)
third.merge(second)
# fsa.draw(third)
