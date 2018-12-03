import graphalgs
import preprocess


def solveOnlyFiber(graph, dijkstraList):
	
	customerList = graph['CustomerNodes']
	assEdge1Cost = costDic[tuple(graph['AssEdges1'][0])]
	
	for assEdge in graph['AssEdges1']:
		if costDic[tuple(assEdge)] != assEdge1Cost:
			raise Exception("assignment costs not consistent")
	
	min_cost = None
	min_root = None
	predecessorDic = {}
	
	for nodeDijkstra in dijkstraList:
		root = nodeDijkstra[0]
		cost = 0
		dicTmp = {}
		
		for cust in customerList:
			facNode = graphalgs.getMinCostFacAssEdge(cust, nodeDijkstra[1], graph['AssEdges1'])
			cost = cost + nodeDijkstra[1][facNode] + assEdge1Cost
			dicTmp[cust] = facNode
		
		if min_cost == None or cost < min_cost:
			min_root = root
			min_cost = cost
			predecessorDic = dicTmp
	
	return min_root, min_cost, predecessorDic