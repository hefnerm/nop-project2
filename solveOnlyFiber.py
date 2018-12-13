import graphalgs
import preprocess


def solveOnlyFiber(graph, dijkstraList, costDic):
	
	customerList = graph['CustomerNodes']
	fiberCost = 0
	for facNode in graph['FacilityNodes']:
		if fiberCost == 0 and facNode[4] == 1:
			fiberCost = costDic[facNode[0]]
		else:
			continue
		if facNode[4] == 1 and costDic[facNode[0]] != fiberCost:
			raise Exception("fiber installation costs not consistent")
	
	min_cost = None
	min_root = None
	predecessorDic = {}
	
	for nodeDijkstra in dijkstraList:
		root = nodeDijkstra[0]
		cost = costDic[root]
		dicTmp = {}
		
		for cust in customerList:
			facNode, edge = graphalgs.getMinCostFacAssEdge(cust, nodeDijkstra[1], graph['AssEdges1'])
			cost = cost + nodeDijkstra[1][facNode] + fiberCost
			dicTmp[cust[0]] = facNode
		
		if min_cost == None or cost < min_cost:
			min_root = root
			min_cost = cost
			predecessorDic = dicTmp
	
	return min_root, min_cost, predecessorDic