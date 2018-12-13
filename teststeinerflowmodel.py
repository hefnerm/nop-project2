import steinerflowmodel
import preprocess
import datanice
import readWrite
import plotSolution
import time

instance = 'v'
demandFactor = 1
yearNumber = 0

dataDic, costDic = readWrite.read(instance)
dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic, demandFactor)

facilitys, steinerNodes, cos, customers, coreEdges, assEdges1, assEdges2 = datanice.datanice(dataDic)

min_root = None
min_costs = None

start_time = time.time()

solution = {}

for root in cos:
	nodesDij = [root] + steinerNodes + facilitys
	if not nodesDij[0] == root:
		nodesDij.remove(root)
		nodesDij.insert(0, root)

	vis, pa = preprocess.dijkstra(nodesDij, coreEdges, root[1], costDic)
	nodesModel = facilitys + customers + [root]

	edgesModel = assEdges1 + assEdges2
	##nShPathes = 0
	for n in facilitys:
		e = ['shortestpath', 'sp_' + root[1] + '_' + n[1] , root[1], n[1]]
		edgesModel.append(e)
		##nShPathes = nShPathes + 1
	
	costsModel = {}
	for n in facilitys:
		if n[5] == 2:
			costsModel[root[1], n[1]] = vis[n[1]] + costDic[n[1]]
		if n[5] == 1:
			costsModel[root[1], n[1]] = vis[n[1]]
	for e in assEdges1:
		costsModel[e[2], e[3]] = costDic[tuple(e)] + costDic[e[2]]
	for e in assEdges2:
		costsModel[e[2], e[3]] = costDic[tuple(e)]

	model, solutionModel = steinerflowmodel.solve_steinerflowmodel(nodesModel, customers, root, edgesModel, costsModel)
	costsfinal = model.ObjVal + costDic[root[1]]
	
	if min_costs == None or min_costs < costsfinal:
		min_costs = costsfinal
		min_root = root
	
	##nAssEdgesUsed = 0
	##nShPEdgesUsed = 0
	##for edge in solutionModel:
	##	if edge[0] == 'assEdge1' or edge[0] == 'assEdge2':
	##		nAssEdgesUsed = nAssEdgesUsed + 1
	##	elif edge[0] == 'shortestpath':
	##		nShPEdgesUsed = nShPEdgesUsed + 1
	##	else:
	##		raise Exception("sth wrong")
	
	##facNodesUsed = []
	##for edge in solutionModel:
	##	if edge[0] == 'assEdge1' or edge[0] == 'assEdge2':
	##		if not edge[2] in facNodesUsed:
	##			facNodesUsed.append(edge[2])
	
	##for facNode in facNodesUsed:
	##	shPathFound = False
	##	for edge in solutionModel:
	##		if edge[0] == 'shortestpath':
	##			if edge[3] == facNode:
	##				shPathFound = True
	##	
	##	if not shPathFound:
	##		print("\nFACNODE IN SOLMODEL NOT ADJACENT TO ROOT\n")
	
	solution[root[1]]=[]
	##nShPathesUsed = 0
	for e in solutionModel:
		if e[0] == 'shortestpath':
			##if e[2] != root[1]:
			##	print("root: ", root)
			##	print("e: ", e)
			##	raise Exception("sth wrong with shortestpath")
			path, length = preprocess.getPathEdgesDij(e[2],e[3],pa,coreEdges)
			##print(length)
			##nShPathesUsed = nShPathesUsed + 1
			for pathEdge in path:
				if not pathEdge in solution[root[1]]:
					solution[root[1]].append(pathEdge)
		else:
			solution[root[1]].append(e)
	
	##for steinerNode in steinerNodes:
	##	steinerNodeHasOutgoingEdge = False
	##	steinerNodeHasIncomingEdge = False
	##	for edge in solution[root[1]]:
	##		if edge[2] == steinerNode[1]:
	##			steinerNodeHasOutgoingEdge = True
	##		if edge[3] == steinerNode[1]:
	##			if steinerNodeHasIncomingEdge:
	##				raise Exception("steiner node has multiple incoming edges")
	##			steinerNodeHasIncomingEdge = True
	##	
	##	if steinerNodeHasOutgoingEdge != steinerNodeHasIncomingEdge:
	##		print(steinerNode)
	##		print("hasOutgoing: ", steinerNodeHasOutgoingEdge)
	##		
	##		raise Exception("steiner node hasIncoming != hasOutgoing")
	##	
	
	##print("nShPathes: ", nShPathes)
	##print("nShPathesUsed: ", nShPathesUsed)
	
	
	##nCustsAssignedVia1 = 0
	##nCustsAssignedVia2 = 0
	
	##for edge in solutionModel:
	##	if edge[0] == 'shortestpath':
	##		if edge[2] != root[1]:
	##			raise Exception("shortest path edge not from root outgoing")
	
	##for cust in customers:
	##	custIsAssigned = False
	##	for edge in solutionModel:
	##		if edge[3] == cust[1]:
	##			if edge[0] == 'assEdge1':
	##				facCorrespondingToUsedEdgeIsAssigned = False
	##				for shPaEdge in solutionModel:
	##					if shPaEdge[0] == 'shortestpath':
	##						if shPaEdge[3] == edge[2]:
	##							if shPaEdge[2] != root[1]:
	##								raise Exception("shPaEdge not from root assigned")
	##							if facCorrespondingToUsedEdgeIsAssigned:
	##								raise Exception("fac double assigned")
	##							facCorrespondingToUsedEdgeIsAssigned = True
	##				if not facCorrespondingToUsedEdgeIsAssigned:
	##					raise Exception("fac not assigned to root")
	##				
	##				nCustsAssignedVia1 = nCustsAssignedVia1 + 1
	##				if custIsAssigned:
	##					raise Exception("cust double assigned")
	##				custIsAssigned = True
	##			if edge[0] == 'assEdge2':
	##				facCorrespondingToUsedEdgeIsAssigned = False
	##				for shPaEdge in solutionModel:
	##					if shPaEdge[0] == 'shortestpath':
	##						if shPaEdge[3] == edge[2]:
	##							if shPaEdge[2] != root[1]:
	##								raise Exception("shPaEdge not from root assigned")
	##							if facCorrespondingToUsedEdgeIsAssigned:
	##								raise Exception("fac double assigned")
	##							facCorrespondingToUsedEdgeIsAssigned = True
	##				if not facCorrespondingToUsedEdgeIsAssigned:
	##					raise Exception("fac not assigned to root")
	##				
	##				nCustsAssignedVia2 = nCustsAssignedVia2 + 1
	##				if custIsAssigned:
	##					raise Exception("cust double assigned")
	##				custIsAssigned = True
	##	
	##	if not custIsAssigned:
	##		raise Exception("cust not assigned")
	
	##print("nCustsAssignedVia1: ", nCustsAssignedVia1)
	##print("nCustsAssignedVia2: ", nCustsAssignedVia2)
	
	
	
	##for cust in customers:
	##	nEdgesForCust = 0
	##	for edge in solution[root[1]]:
	##		if edge[3] == cust[1]:
	##			nEdgesForCust = nEdgesForCust + 1
	##	
	##	if nEdgesForCust != 1:
	##		print("\n\nNUMBER ASSEDGES FOR CUST WRONG\n\n")
	
	
	#for edge in solution[root[1]]:
	#	if edge[0] == 'coreEdge':
	#		print(edge)

	#print('\n', 'CO: ', root[1], ':', costsfinal)
	#plotSolution.plotSolution(facilitys, steinerNodes, cos, customers, solution[root[1]], root)

print("min_co: ", min_root[1], " min_costs: ", min_costs)

elapsed_time = time.time() - start_time
print("time: ", elapsed_time, "s")
plotSolution.plotSolution(facilitys, steinerNodes, cos, customers, solution[min_root[1]], min_root)