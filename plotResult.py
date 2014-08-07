#Script for plotting some stuff

import world
import reinforceClass
import reinforceM1
import reinforceM2
import reinforceM3
import mathtool
import pylab


myMaze = world.Maze(rows = 5, columns = 3, mazeType = 'price', objPos = [4,0])
myMaze.drawSelf(isnew = True)
myAgent = reinforceClass.Agent([3,0])
myAgent.drawSelf(myMaze.window, True, color = 'green')
myAgent = reinforceClass.Agent([2,0])
myAgent.drawSelf(myMaze.window, True, color = 'red')
myAgent = reinforceClass.Agent([1,0])
myAgent.drawSelf(myMaze.window, True, color = 'skyblue')
myAgent = reinforceClass.Agent([0,0])
myAgent.drawSelf(myMaze.window, True, color = 'purple')
#predator = reinforceClass.Predator([1,1])
#predator.drawSelf(myMaze.window, True)

#QtableM3 = mathtool.readQFromFile('Q3.txt',"M3")
#reinforceM3.printQtable_M3(QtableM3)
QtableM1 = mathtool.readQFromFile('Q1.txt',"M1")
#reinforceM3.printQtable_M3(QtableM3)


def queryQtable(Qtable,objRelPos):
    agentPos = [0,0]
    state = reinforceM1.stateMapping_M1(agentPos,objRelPos)
    return Qtable[state[0]][state[1]]

Qvalues = []
for i in range(5):
    Qvalues.append(queryQtable(QtableM1,[i,0]))
    pylab.plot([0,1,2,3],Qvalues[i],'-o')
    print(Qvalues[i])

pylab.show()


raw_input("press enter to exit")
