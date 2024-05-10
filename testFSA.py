import fsa

behavior = fsa.FSA()

behavior.addState('IDLE')
behavior.addState('MOVING')

behavior.addEdge('IDLE', 'MOVING', {'paramA': 0, 'paramB': 1})
behavior.addEdge('MOVING', 'IDLE', {'paramA': 1, 'paramB': 0})

# print(behavior.getCurrState())

behavior.next({'paramA': 1, 'paramB': 0})
# print(behavior.getCurrState())

behavior.next({'paramA': 0, 'paramB': 1})
# print(behavior.getCurrState())

behavior.next({'paramA': 0, 'paramB': 1})
# print(behavior.getCurrState())

behavior.next({'paramA': 1, 'paramB': 0})
# print(behavior.getCurrState())

behavior.next({'paramA': 0, 'paramB': 1})
# print(behavior.getCurrState())

behavior.reset()
# print(behavior.getCurrState())

behavior.setInitialState('MOVING')
behavior.reset()
# print(behavior.getCurrState())

behavior.draw()
