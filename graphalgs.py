#input: node and edges of a graph
#output: all outgoing edges of the node in the graph
def outgoing(node, edges):
	outgoingEdges = []
	for e in edges:
		if (e[2] == node):
			outgoingEdges.append(e)

	return outgoingEdges

#input: node and edges of a graph
#output: all incomming edges of the node in the graph
def incoming(node, edges):
	incomingEdges = []
	for e in edges:
		if (e[3] == node):
			incomingEdges.append(e)

	return incomingEdges

#input: cust: customer, dijkstra: dictionary with all facility nodes and the length of the path to this node, assEdges: list of all assignment edges
#output: a facility node adjacent to cust with the minimal costs of getting to the facility node from the root; the corresponding assignment edge 
def getMinCostFacAssEdge(cust, dijkstra, assEdges):
	min_fac = None
	min_edge = None
	
	for edge in assEdges:
		if edge[3] == cust:
			
			#save the node with minimal costs
			if min_fac == None:
				min_fac = edge[2]
				min_edge = edge
			elif dijkstra[edge[2]] < dijkstra[min_fac]:
				min_fac = edge[2]
				min_edge = edge
	
	if min_fac == None:
		raise Exception("no adjacent facility node found")
	
	return min_fac, min_edge

def getFather(solution, node, child):
	print("in getFather")
	print("node: ", node)
	print("child: ", child)
	print("sol[0]: ",solution[0])
	for edge in solution:
		if node in edge:
			print("edge found!", edge)
	
	#print(solution)
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
	node = terminal
	child = None
	
	print("input root: ", root)
	print("input terminal: ", terminal)
	
	while node != root:
		print("node: ", node)
		#print("node: ", node)
		if node == terminal:
			father = getFather(solution, node, None)
			print("father (n=t): ", father)
			if father == -1:
				return -1
		else:
			father = getFather(solution, node, child)
			print("father (n!=t): ", father)
			if father == -1:
				return -1
		#print("father: ", father)
		path.insert(0, node)
		child = node
		node = father
		#print(path)
	
	path.insert(0, root)
	#print(path)
	return path