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

nodesreduced=

#print(roots)
#print(customers)
#Knoten CO+Facilitys+Customers
#nodes=[1,2,3,4,5,6,7,8,9,10,11,12]
#Customers
#terminals=[9,10,11,12]
#CO
#root=1
#Kanten: Co->Facilities+ alle assignment edges
#edges=[[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[2,9],[2,10],[2,11],[2,12],[3,9],[4,10],[5,10],[6,11],[6,12],[7,11],[8,12]]

#Kosten: Co->Facitlites2: Wegkosten+Multiplexeraufbau, Co-> Facilities1: Wegkosten, Facilites2->Customers: Kupferkosten, Facilties1 -> Customers: Glasfaseranschlusskosten (1500)
#costs={(1,2):4900,(1,3):18400,(1,4):20900,(1,5):24000,(1,6):10500,(1,7):17600,(1,8):22400,(2,9):110,(2,10):110,(2,11):110,(2,12):110,(3,9):1500,(4,10):110,(5,10):1500,(6,11):110,(6,12):110,(7,11):1500,(8,12):1500}


for root in cos:
	nodesreduced=


#	model,solution=steinerflowmodel.solve_steinerflowmodel(nodesreduced,customers,root,edgesreduced,costs)
#print(solution) 