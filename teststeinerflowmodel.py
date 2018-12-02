#dijkstra per hand
#knoten per hand usw

import steinerflowmodel


import readWrite

dataDic, costDic = readWrite.read('n')

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

facilitys,steinerNodes,cos,customers,coreEdges,assEdges1,assEdges2=datanice(dataDic)


for root in cos:
	nodesreduced=root+facilitys+customers
	edgesreduced=assEdges1+assEdges2
	for n in facilitys:
		e=['shortestpath', 'sp_'+ root[1] +'_'+n[1] , root[1],n[1]]
		edgesreduced.append(e)

#####################################################
# hier fehlen die kosten für den bums

#Kosten: Co->Facitlites2: Wegkosten+Multiplexeraufbau, Co-> Facilities1: Wegkosten, Facilites2->Customers: Kupferkosten, Facilties1 -> Customers: Glasfaseranschlusskosten (1500)
####################################################

#	model,solution=steinerflowmodel.solve_steinerflowmodel(nodesreduced,customers,root,edgesreduced,costs)
#print(solution) 