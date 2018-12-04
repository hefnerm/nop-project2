#dijkstra per hand
#knoten per hand usw

import steinerflowmodel
import preprocess
import datanice
import readWrite
import plotSolution


dataDic, costDic = readWrite.read('b')
dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic)

facilitys,steinerNodes,cos,customers,coreEdges,assEdges1,assEdges2=datanice.datanice(dataDic)
solution={}	
###########costest normal nicht
costest=[cos[0]]
for root in costest:
	nodesDij=cos+steinerNodes+facilitys

	vis, pa = preprocess.dijkstra(nodesDij, coreEdges, root, costDic)
	
	nodesModel=facilitys+customers+[root]
	edgesModel=assEdges1+assEdges2
	for n in facilitys:
		e=['shortestpath', 'sp_'+ root[1] +'_'+n[1] , root[1],n[1]]
		edgesModel.append(e)
	
	costsModel={}
	for n in facilitys:
		if n[5]==2:
			costsModel[root[1],n[1]]=vis[n[1]]+costDic[n[1]]
		if n[5]==1:
			costsModel[root[1],n[1]]=vis[n[1]]
	for e in assEdges1:
		costsModel[e[2],e[3]]=costDic[tuple(e)]+costDic[e[2]]
	for e in assEdges2:
		costsModel[e[2],e[3]]=costDic[tuple(e)]

	model,solutionModel=steinerflowmodel.solve_steinerflowmodel(nodesModel,customers,root,edgesModel,costsModel)
	costsfinal=model.ObjVal+costDic[root[1]]

	solution[root[1]]=[]
	for e in solutionModel:
		if e[0]=='shortestpath':
			path=preprocess.getPathEdgesDij(e[2],e[3],pa,coreEdges)
			solution[root[1]]=solution[root[1]]+path
		else:
			solution[root[1]].append(e)

	print('\n','CO: ',root[1],':', costsfinal)
	plotSolution.plotSolution(facilitys,steinerNodes,cos,customers,solution[root[1]],root)

print(solution)