#Script for plotting some stuff

import world
import reinforcement 
import mathtool
import pylab


#myMaze = world.Maze(rows = 2, columns = 4, mazeType = 'price', objPos = [0,3])
#myMaze.drawSelf(isnew = True)
#myAgent = reinforcement.Agent([1,0])
#myAgent.drawSelf(myMaze.window, True)


QtableM1 = mathtool.readQFromFile('Q1_VRANGE_3Q.txt',"M1")

def queryQtable(Qtable,objRelPos):
    agentPos = [0,0]
    state = reinforcement.stateMapping_M1(agentPos,objRelPos)
    return Qtable[state[0]][state[1]]

Qvalues = []
for i in range(4):
    Qvalues.append(queryQtable(QtableM1,[0,i]))
    pylab.plot([0,1,2,3],Qvalues[i],'-o')
    print(Qvalues[i])

pylab.show()


raw_input("press enter to exit")
