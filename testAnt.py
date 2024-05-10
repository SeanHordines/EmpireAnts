import ant

testAnt = ant.ant((0, 0, 0))

print(testAnt)

print(f"facing: %d" % testAnt.turn(2))
print(f"coords: (%d, %d, %d)" % testAnt.move())

pheromone = 'test'
strength = testAnt.detect({}, 'test')
print(f"strength of %s at %s: %.2f" % (pheromone, testAnt.getPos()[0], strength))
strength = testAnt.detect({'test': 5}, 'test')
print(f"strength of %s at %s: %.2f" % (pheromone, testAnt.getPos()[0], strength))
