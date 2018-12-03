import graphalgs

def deleteAssEdgesP2P(dataDic, costDic):
	
	vertices = dataDic['nodes']
	
	toDelete = []
	
	for cust in vertices:
		if cust[0] != 'customer':
			continue
		
		demand = cust[4]
		
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

def deleteCusts(nodes, edges):
	
	newNodes = []
	newEdges = []
	return newNodes, newEdges


def dijkstra(nodes, edges, root, costDic):
	visited = {root[1]: 0}
	path = {}

	nodesTmp = nodes
	
	while nodesTmp: 
		#print("\nin nodesTmp\n")
		min_node = None
		for node in nodesTmp:
			#print("\n in for")
			#print(node[1])
			if node[1] in visited:
				#print("visited\n")
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