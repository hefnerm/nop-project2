def outgoing(node, edges):
	outgoingEdges = []
	for e in edges:
		if (e[2] == node):
			outgoingEdges.append(e)

	return outgoingEdges


def incoming(node, edges):
	incomingEdges = []
	for e in edges:
		if (e[3] == node):
			incomingEdges.append(e)

	return incomingEdges

def getMinCostFacAssEdge(cust, dijkstra, assEdges):
	min_fac = None
	
	for edge in assEdges:
		if edge[2] == cust:
			if min_fac == None:
				min_fac = dijkstra[edge[1]]
			elif dijkstra[edge[1]] < dijkstra[min_fac]:
				min_fac = edge[1]
	
	if min_fac == None:
		raise Exception("no adjacent facility node found")
	
	return min_fac