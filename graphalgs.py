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
		if edge[2] == cust[0]:
			if min_fac == None:
				min_fac = edge[1]
			elif dijkstra[edge[1]] < dijkstra[min_fac]:
				min_fac = edge[1]
	
	if min_fac == None:
		raise Exception("no adjacent facility node found")
	
	return min_fac

def getFather(solution, node, child):
	for edge in solution:
		if child == None:
			if edge[3] == node:
				return edge[2]
		else:
			if edge[3] == node and edge[2] != child:
				return edge[2]
	
	return -1

def getPathP2MP(solution, root, terminal):
	path = []
	father = None
	node = terminal[1]
	child = None
	
	while node != root[1]:
		#print("node: ", node)
		if node == terminal:
			father = getFather(solution, node, None)
			if father == -1:
				return -1
		else:
			father = getFather(solution, node, child)
			if father == -1:
				return -1
		#print("father: ", father)
		path.insert(0, node)
		child = node
		node = father
		#print(path)
	
	path.insert(0, root[1])
	#print(path)
	return path