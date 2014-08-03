#Script for plotting some stuff

import world
import reinforceClass
import reinforceM1
import reinforceM2
import reinforceM3
import mathtool
import pylab


myMaze = world.Maze(rows = 9, columns = 9, mazeType = 'test')
myMaze.drawSelf(isnew = True)
myAgent = reinforceClass.Agent([4,2])
myAgent.drawSelf(myMaze.window, True)
predator = reinforceClass.Predator([7,6])
predator.drawSelf(myMaze.window, True)

#QtableM1 = mathtool.readQFromFile('Q1_VRANGE_3Q.txt',"M1")
#reinforceM1.printQtable_M1(QtableM1)
#
#def queryQtable(Qtable,objRelPos):
#    agentPos = [0,0]
#    state = reinforceM1.stateMapping_M1(agentPos,objRelPos)
#    return Qtable[state[0]][state[1]]
#
#Qvalues = []
#for i in range(4):
#    Qvalues.append(queryQtable(QtableM1,[0,i]))
#    pylab.plot([0,1,2,3],Qvalues[i],'-o')
#    print(Qvalues[i])
#
#pylab.show()


raw_input("press enter to exit")
