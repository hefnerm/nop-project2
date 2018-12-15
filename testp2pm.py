import preprocess
import datanice
import readWrite
import plotSolution
import p2mpmodel
import graphalgs

#########################################################NEUES EINLESEN
dataDic, costDic, profitDic = readWrite.read('b')
dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic, 1)

edges=dataDic['edges']
facilitys,steinerNodes,cos,customers,coreEdges,assEdges1,assEdges2=datanice.datanice(dataDic)

for e in coreEdges:
	flag=False
	for c in cos:
		if e[2] == c[1]:
			flag=True
	if not flag:
		edges.append([e[0],e[1],e[3],e[2],e[4],e[5]])
		costDic[e[0],e[1],e[3],e[2],e[4],e[5]]=costDic[tuple(e)]

dataDic['edges']=edges

nodes = dataDic['nodes']

facilitys,steinerNodes,cos,customers,coreEdges,assEdges1,assEdges2=datanice.datanice(dataDic)


facilitys1=[]
facilitys2=[]
#need the following only for debugging
facilitiesOnlyNames1 = []
facilitiesOnlyNames2 = []
customersOnlyNames = []
for f in facilitys:
	if f[5]==1:
		facilitys1.append(f)
		facilitiesOnlyNames1.append(f[1])
	else:
		facilitys2.append(f)
		facilitiesOnlyNames2.append(f[1])

for cust in customers:
	customersOnlyNames.append(cust[1])


############################splitngnumber=1 sollte lösung für p2p ergeben#####################################
splittingNumber=4

###Splitter costs calculation
summ=0
numberOfCoreEdges=0
for e in coreEdges:
	summ=summ+costDic[tuple(e)]
	numberOfCoreEdges=numberOfCoreEdges+1
splitterCosts=(summ/numberOfCoreEdges)/2


###############################################NEUES EINLESEN#####################################################################################

timelimit=1000000000000

min_root = None
min_costs = None

#coEdges = []
#for co in cos:
#	for e in coreEdges:
#			if e[2] == co[1]:
#			coEdges.append(e)

for root in cos:
	coreEdgesNew = []
	for e in coreEdges:
		flag = False
		for c in cos:
			if c[1] != root[1]:
				if (e[2] == c[1]):
					flag = True
		if not flag:
			coreEdgesNew.append(e)

	model,x,y,s,m,solutionModel = p2mpmodel.solve_P2MPModel(nodes,edges,root,cos,facilitys,facilitys1,facilitys2,customers,steinerNodes,coreEdgesNew,assEdges1,assEdges2,costDic,splittingNumber,splitterCosts,timelimit)
	considered = []
	mltplEdges = []
	for e in edges:
		if not [e[3], e[2]] in considered and not root[1] in [e[2], e[3]] and not e[0] in ['assEdge1', 'assEdge2']:
			if x[e[2], e[3]].X > 0 and x[e[3], e[2]].X > 0:
				print("double edge found! e: ", e)
				print("x[", e[2], ", ", e[3],"] = ", x[e[2], e[3]].X)
				print("x[", e[3], ", ", e[2],"] = ", x[e[3], e[2]].X)
				mltplEdges.append(e)
			considered.append([e[2], e[3]])
	
	for e in mltplEdges:
		nodeFirst = e[2]
		nodeSecond = e[3]
		incListFirst = []
		incListSec = []
		for e2 in edges:
			if nodeFirst in [e2[2], e2[3]]:
				incListFirst.append(e2)
			if nodeSecond in [e2[2], e2[3]]:
				incListSec.append(e2)
		
		print("nodeFirst: ", nodeFirst)
		if nodeFirst in facilitiesOnlyNames2:
			print("m[", nodeFirst, "] = ", m[nodeFirst].X)
		else:
			print(nodeFirst, " not able to install multiplexer")
		
		if not nodeFirst in customersOnlyNames:
			print("s[", nodeFirst, "] = ", s[nodeFirst].X)
		else:
			print(nodeFirst, " is customer")
			raise Exception("thats quite strange")
		print("incidentListFirst: ", incListFirst)
		for incEdge in incListFirst:
			print("incidentEdge to first node: ", incEdge, " of type: ", incEdge[0])
			print("x[", incEdge[2], ", ", incEdge[3], "] = ", x[incEdge[2], incEdge[3]].X)
			if not incEdge[0] in ['assEdge1', 'assEdge2']:
				print("x[", incEdge[3], ", ", incEdge[2], "] = ", x[incEdge[3], incEdge[2]].X)
			if nodeFirst == incEdge[2]:
				adjNode = incEdge[3]
			else:
				adjNode = incEdge[2]
			
			if adjNode in facilitiesOnlyNames2:
				print("m[", adjNode, "] = ", m[adjNode].X)
			else:
				print(adjNode, " not able to install multiplexer")
			
			if not adjNode in customersOnlyNames:
				print("s[", adjNode, "] = ", s[adjNode].X)
			else:
				print(adjNode, " is customer")
		
		print("nodeSecond: ", nodeSecond)
		if nodeSecond in facilitiesOnlyNames2:
			print("m[", nodeSecond, "] = ", m[nodeSecond].X)
		else:
			print(nodeSecond, " not able to install multiplexer")
		
		if not nodeSecond in customersOnlyNames:
			print("s[", nodeSecond, "] = ", s[nodeSecond].X)
		else:
			print(nodeSecond, " is customer")
		
		print("incidentListSec: ", incListSec)
		for incEdge in incListSec:
			print("incidentEdge to second node: ", incEdge, " of type: ", incEdge[0])
			print("x[", incEdge[2], ", ", incEdge[3], "] = ", x[incEdge[2], incEdge[3]].X)
			if not incEdge[0] in ['assEdge1', 'assEdge2']:
				print("x[", incEdge[3], ", ", incEdge[2], "] = ", x[incEdge[3], incEdge[2]].X)
			if nodeSecond == incEdge[2]:
				adjNode = incEdge[3]
			else:
				adjNode = incEdge[2]
			
			if adjNode in facilitiesOnlyNames2:
				print("m[", adjNode, "] = ", m[adjNode].X)
			else:
				print(adjNode, " not able to install multiplexer")
			
			if not adjNode in customersOnlyNames:
				print("s[", adjNode, "] = ", s[adjNode].X)
			else:
				print(adjNode, " is customer")
			
	edgeNumberDic={}
	for e in solutionModel:
		edgeNumberDic[e[2],e[3]]=x[e[2],e[3]].X

	#plotSolution.plotSolution(facilitys,steinerNodes,cos,customers,solutionModel,root,edgeNumberDic,m,s,False)


	costsfinal = model.ObjVal + costDic[root[1]]
	print(root[1], " : ", costsfinal)

	if min_costs == None or costsfinal < min_costs:
		min_costs = costsfinal
		min_root = root
		min_solution = solutionModel
		minEdgeNumberDic = edgeNumberDic


plotSolution.plotSolution(facilitys,steinerNodes,cos,customers,min_solution,root,minEdgeNumberDic,m,s,False)
