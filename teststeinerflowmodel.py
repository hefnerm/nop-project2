#dijkstra per hand
#knoten per hand usw

import steinerflowmodel
import preprocess
import datanice
import readWrite


dataDic, costDic = readWrite.read('n')
dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic)

facilitys,steinerNodes,cos,customers,coreEdges,assEdges1,assEdges2=datanice.datanice(dataDic)
for root in cos:
	nodesDij=cos+steinerNodes+facilitys

	vis, pa = preprocess.dijkstra(nodesDij, coreEdges, cos[0], costDic)
	nodesModel=facilitys+customers
	if not (root in nodesModel):
		nodesModel.append(root)

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

	model,solution=steinerflowmodel.solve_steinerflowmodel(nodesModel,customers,root,edgesModel,costsModel)
	costsfinal=model.ObjVal+costDic[root[1]]
	print('\n','CO: ',root[1],':', costsfinal)