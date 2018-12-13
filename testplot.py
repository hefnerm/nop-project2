import preprocess
import datanice
import readWrite
import plotSolution

dataDic, costDic = readWrite.read('v')
dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic,1)

facilitys,steinerNodes,cos,customers,coreEdges,assEdges1,assEdges2=datanice.datanice(dataDic)

plotSolution.plotSolution(facilitys,steinerNodes,cos,customers,dataDic['edges'],cos[0])