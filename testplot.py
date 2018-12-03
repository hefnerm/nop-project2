import steinerflowmodel
import preprocess
import datanice
import readWrite
import plotSolution

dataDic, costDic = readWrite.read('n')
dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic)

facilitys,steinerNodes,cos,customers,coreEdges,assEdges1,assEdges2=datanice.datanice(dataDic)

plotSolution.plotSolution(facilitys,steinerNodes,cos,customers,coreEdges,cos[0])