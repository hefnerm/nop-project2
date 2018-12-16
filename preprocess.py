import graphalgs

#input: dataDic dictionary with graph data; costDic cost dictionary for vertices and edges; demandFactor factor the demand of each customers has grown
#output: dataDic without the assignment edges that can not contain the full demand of the customer
def deleteAssEdgesP2P(dataDic, costDic, demandFactor):
	
	vertices = dataDic['nodes']
	
	#list of edges that have to be deleted
	toDelete = []
	
	for cust in vertices:
		if cust[0] != 'customer':
			continue
		
		demand = cust[4] * demandFactor
		
		for edge in dataDic['edges']:
			if edge[0] != 'assEdge2':
				continue
			if edge[3] != cust[1]:
				continue
			
			if edge[5] < demand:
				toDelete.append(edge)
	
	for edge in toDelete:
		dataDic['edges'].remove(edge)
		tmp = [edge[1], edge[2], edge[3], costDic[tuple(edge)], edge[4], edge[5]]
		dataDic['AssEdges2'].remove(tmp)
	
	return dataDic


#input: startNode the node the path starts; endNode the node the path ends in; pathDij dictionary that contains the parent in the dijkstra-tree for every node; edges the list of all edges of the graph
#output: the list of the edges forming the path und its length
def getPathEdgesDij(startNode, endNode, pathDij, edges):
	tempPathEdges = []
	pathEdges = []	
	
	tempNode1 = endNode
	tempNode2 = pathDij[endNode]
	tempPathEdges.append([tempNode2, tempNode1])
	
	length = 1
	
	#iterate until the startNode is reached
	while tempNode2 != startNode:
		tempNode1 = tempNode2
		tempNode2 = pathDij[tempNode1]
		tempPathEdges.append([tempNode2, tempNode1])
		
		length = length + 1
	
	##TODO## nicht cool das so durch zu gehen...
	#search for the corresponding edges of the graph
	for e in edges:
		for t in tempPathEdges:
			if (e[2] == t[0] and e[3] == t[1]) or (e[2] == t[1] and e[3] == t[0]):
				pathEdges.append(e)
	
	return pathEdges, length

#input: nodes is the list of nodes of the graph; edges the list of all edges; root is the node to start dijkstra on and for which we want to know all shortest paths; costDic is the dictionary containing the costs of all edges
#output: a dictionary containing the length of a shortest way from root to the node and a dictionary with the parent node in the dijkstra-tree
#dijkstras algorithm for computing a shortest path from a root to every other node
def dijkstra(nodes, edges, root, costDic):
	visited = {root: 0}
	path = {}

	nodesTmp = nodes.copy()
	
	#as long as not all nodes are visited
	while nodesTmp:
		min_node = None
		for node in nodesTmp:
			if node[1] in visited:
				if min_node is None:
					min_node = node[1]
				elif visited[node[1]] < visited[min_node]:
					min_node = node[1]
		
		if min_node is None:
			break
		
		for node in nodesTmp:
			if node[1] == min_node:
				nodesTmp.remove(node)
				break
		
		current_weight = visited[min_node]
		
		edgesTmp = graphalgs.incoming(min_node, edges) + graphalgs.outgoing(min_node, edges)
		
		for edge in edgesTmp:
			weight = current_weight + costDic[tuple(edge)]
			
			if min_node == edge[2]:
				adjNode = edge[3]
			else:
				adjNode = edge[2]
				
			if adjNode not in visited or weight < visited[adjNode]:
				visited[adjNode] = weight
				path[adjNode] = min_node
	
	return visited, path

#input: nodes is the list of nodes of the graph; edges the list of all edges; root is the node to start dijkstra on and for which we want to know all shortest paths; costDic is the dictionary containing the costs of all edges
#output: a dictionary containing the length of a shortest way from root to the node and a dictionary with the parent node in the dijkstra-tree
#dijkstras algorithm for computing a shortest path from a root to every other node
def dijkstra2(nodes, edges, root, costDic):
	visited = {root: 0}
	path = {}
	
	nodesTmp = nodes.copy()
	
	while nodesTmp: 
		min_node = None
		for node in nodesTmp:
			if node[1] in visited:
				if min_node is None:
					min_node = node
				elif visited[node[1]] < visited[min_node[1]]:
					min_node = node
		
		if min_node is None:
			break
		
		for node in nodesTmp:
			if node == min_node:
				nodesTmp.remove(node)
				break
		
		current_weight = visited[min_node[1]]
		
		edgesTmp = graphalgs.incoming(min_node[1], edges) + graphalgs.outgoing(min_node[1], edges)
		
		for edge in edgesTmp:
			weight = current_weight + costDic[tuple(edge)]
			
			if min_node[1] == edge[2]:
				adjNode = edge[3]
			else:
				adjNode = edge[2]
				
			if adjNode not in visited or weight < visited[adjNode]:
				visited[adjNode] = weight
				path[adjNode] = min_node[1]
	
	return visited, path