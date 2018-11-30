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