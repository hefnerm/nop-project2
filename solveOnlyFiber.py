import graphalgs
import preprocess
#input: 
#output:
def solveOnlyFiber(graph, facilities, customers, assEdges1, dijkstraList, costDic):
	
	fiberCost = None
	for facNode in facilities:
		if fiberCost == None and facNode[5] == 1:
			fiberCost = costDic[facNode[1]]
		else:
			continue
		if facNode[5] == 1 and costDic[facNode[1]] != fiberCost:
			raise Exception("fiber installation costs not consistent")
	
	min_cost = None
	min_root = None
	predecessorDic = {}
	
	for nodeDijkstra in dijkstraList:
		root = nodeDijkstra[0]
		cost = costDic[root]
		dicTmp = {}
		edgeList = []
		
		#for cust in customerList:
		for cust in customers:
			facNode, edge = graphalgs.getMinCostFacAssEdge(cust[1], nodeDijkstra[1], assEdges1)
			cost = cost + nodeDijkstra[1][facNode] + fiberCost
			dicTmp[cust[1]] = facNode
			edgeList.append(edge)
		
		if min_cost == None or cost < min_cost:
			min_root = root
			min_cost = cost
			predecessorDic = dicTmp
			solution = edgeList
	
	return min_root, min_cost, predecessorDic, solution