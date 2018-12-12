import readWrite
import preprocess
import graphalgs
import time
import datanice

start_time = time.time()

dataDic, costDic = readWrite.read('n')

dataDic = preprocess.deleteAssEdgesP2P(datDic, costDic, 1)

facilities, steinerNodes, cos, customer, coreEdges, assEdges1, assEdges2 = datanice.datanice(dataDic)

splitterCosts = 0

for cEdge in coreEdges:
	splitterCosts = splitterCosts + costDic[cEdge]

splitterCosts = splitterCosts/2

for root in cos:
	
	modelCosts = {}
	for edge in coreEdges:
		modelCosts[edge[2], edge[3]] = costDic[edge]
	
	for edge in assEdges1:
		
	
	for edge in assEdges2:
		
	
	for node in facilities:
		
	
	
	
	

elapsed_time = time.time() - start_time
print("time: ", elapsed_time, "s")