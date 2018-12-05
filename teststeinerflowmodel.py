#dijkstra per hand
#knoten per hand usw

import steinerflowmodel
import preprocess
import datanice
import readWrite
import plotSolution


dataDic, costDic = readWrite.read('v')
dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic)

facilitys,steinerNodes,cos,customers,coreEdges,assEdges1,assEdges2=datanice.datanice(dataDic)

solution={}	
###########costest normal nicht
costest = [cos[0]]
for root in cos:
	nodesDij = cos + steinerNodes + facilitys
	if not nodesDij[0] == root:
		nodesDij.remove(root)
		nodesDij.insert(0, root)

	vis, pa = preprocess.dijkstra(nodesDij, coreEdges, root[1], costDic)
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
	#plotSolution.plotSolution(facilitys,[],[root],customers,solutionModel,root)

	
	#print(solutionModel)
	nAssEdgesUsed = 0
	nShPEdgesUsed = 0
	for edge in solutionModel:
		if edge[0] == 'assEdge1' or edge[0] == 'assEdge2':
			nAssEdgesUsed = nAssEdgesUsed + 1
		if edge[0] == 'shortestpath':
			nShPEdgesUsed = nShPEdgesUsed + 1
	
	#print("number customers: ",len(customers))
	#print("number assEdges used: ",nAssEdgesUsed)
	#print("number shortestpath edges used: ", nShPEdgesUsed)
	
	facNodesUsed = []
	for edge in solutionModel:
		if edge[0] == 'assEdge1' or edge[0] == 'assEdge2':
			if not edge[2] in facNodesUsed:
				facNodesUsed.append(edge[2])
	
	for facNode in facNodesUsed:
		shPathFound = False
		for edge in solutionModel:
			if edge[0] == 'shortestpath':
				if edge[3] == facNode:
					shPathFound = True
		
		if not shPathFound:
			print("\nFACNODE NOT IN SOLMODEL ADJACENT TO ROOT\n")
	
	#print("facnodesused: ",len(facNodesUsed))
	
	solution[root[1]]=[]
	for e in solutionModel:
		if e[0]=='shortestpath':
			path=preprocess.getPathEdgesDij(e[2],e[3],pa,coreEdges)
			for pathEdge in path:
				if not pathEdge in solution[root[1]]:
					solution[root[1]].append(pathEdge)
		else:
			solution[root[1]].append(e)
	
	for cust in customers:
		nEdgesForCust = 0
		for edge in solution[root[1]]:
			if edge[3] == cust[1]:
				nEdgesForCust = nEdgesForCust + 1
		
		if nEdgesForCust != 1:
			print("\n\nNUMBER ASSEDGES FOR CUST WRONG\n\n")
	
	
	#for edge in solution[root[1]]:
	#	if edge[0] == 'coreEdge':
	#		print(edge)

	print('\n','CO: ',root[1],':', costsfinal)
	plotSolution.plotSolution(facilitys,steinerNodes,cos,customers,solution[root[1]],root)

#print(solution)