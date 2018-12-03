def datanice(dataDic):
	nodes=dataDic['nodes']
	edges=dataDic['edges']

	facilitys=[]
	for n in nodes:
		if n[0]=='facility':
			facilitys.append(n)
	steinerNodes=[]
	for n in nodes:
		if n[0]=='steiner':
			steinerNodes.append(n)
	cos=[]
	for n in nodes:
		if n[0]=='co':
			cos.append(n)
	customers=[]
	for n in nodes:
		if n[0]=='customer':
			customers.append(n)

	coreEdges=[]
	for e in edges:
		if e[0]=='coreEdge':
			coreEdges.append(e)

	assEdges1=[]
	for e in edges:
		if e[0]=='assEdge1':
			assEdges1.append(e)

	assEdges2=[]
	for e in edges:
		if e[0]=='assEdge2':
			assEdges2.append(e)

	return facilitys,steinerNodes,cos,customers,coreEdges,assEdges1,assEdges2