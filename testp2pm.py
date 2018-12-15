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
for f in facilitys:
	if f[5]==1:
		facilitys1.append(f)
	else:
		facilitys2.append(f)


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

for root in [cos[1]]:
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
	
	edgeNumberDic={}
	for e in solutionModel:
		edgeNumberDic[e[2],e[3]]=x[e[2],e[3]].X

	plotSolution.plotSolution(facilitys,steinerNodes,cos,customers,solutionModel,root,edgeNumberDic,m,s,False)


	costsfinal = model.ObjVal + costDic[root[1]]
	print(root[1], " : ", costsfinal)

	if min_costs == None or min_costs < costsfinal:
		min_costs = costsfinal
		min_root = root
		min_solution = solutionModel
		minEdgeNumberDic = edgeNumberDic


plotSolution.plotSolution(facilitys,steinerNodes,cos,customers,min_solution,root,minEdgeNumberDic,m,s,False)
