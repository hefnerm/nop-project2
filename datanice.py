def datanice(dataDic):
	nodes=dataDic['nodes']
	edges=dataDic['edges']

	facilitys=[]
	steinerNodes=[]
	cos=[]
	customers=[]

	for n in nodes:
		if n[0]=='facility':
			facilitys.append(n)
		elif n[0]=='steiner':
			steinerNodes.append(n)
		elif n[0]=='co':
			cos.append(n)
		elif n[0]=='customer':
			customers.append(n)

	coreEdges=[]
	assEdges1=[]
	assEdges2=[]

	for e in edges:
		if e[0]=='coreEdge':
			coreEdges.append(e)
		elif e[0]=='assEdge1':
			assEdges1.append(e)
		elif e[0]=='assEdge2':
			assEdges2.append(e)

	return facilitys,steinerNodes,cos,customers,coreEdges,assEdges1,assEdges2