#Train modules
#Modular RL Project
#Ruohan Zhang

from reinforceM1 import *
from reinforceM2 import *
from reinforceM3 import *
import mathtool

trainM1 = False
trainM2 = False
trainM3 = True

if (trainM1 == True):
    QtableM1 = train_M1()
    filenameM1 = 'Q1.txt'
    mathtool.writeQToFile(QtableM1,filenameM1)
    mathtool.writeTrainParamsToFile('M1',filenameM1)
    QtableM1 = mathtool.readQFromFile(filenameM1,'M1')
    printPolicy_M1(QtableM1,[2,2])
    printQtable_M1(QtableM1)

if (trainM2 == True):
    QtableM2 = train_M2()
    filenameM2 = 'Q2.txt'
    mathtool.writeQToFile(QtableM2,filenameM2)
    mathtool.writeTrainParamsToFile('M2',filenameM2)
    QtableM2 = mathtool.readQFromFile(filenameM2,'M2')
    printPolicy_M2(QtableM2,[3,3])
    printQtable_M2(QtableM2)

if (trainM3 == True):
    QtableM3 = train_M3()
    filenameM3 = 'Q3.txt'
    mathtool.writeQToFile(QtableM3,filenameM3)
    mathtool.writeTrainParamsToFile('M3',filenameM3)
    QtableM3 = mathtool.readQFromFile(filenameM3,'M3')
    printQtable_M3(QtableM3)
