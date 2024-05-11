import ant
import fsa

testAnt = ant.ant((0, 0, 0))

behavior = fsa.FSA("test1", "D:/Sean/programmingshit/EmpireAnts/sampleFSA1.json")
testAnt.setBehavior(behavior)
# fsa.draw(testAnt.behavior)
testAnt.act()
testAnt.next({'paramA': 1})
print(testAnt.act())
