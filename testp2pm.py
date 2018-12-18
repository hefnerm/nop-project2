import preprocess
import datanice
import readWrite
import plotSolution
import p2mpmodel
import graphalgs
import time


def solve_p2mp(instance,demandFactor,period, splittingNumber, timelimit):
	
	dataDic, costDic, profitDic = readWrite.read(instance)
	dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic, demandFactor)
	
	edges = dataDic['edges']

	facilitys, steinerNodes, cos, customers, coreEdges, assEdges1, assEdges2 = datanice.datanice(dataDic)

	#splittercosts calculation
	sum = 0
	numberOfCoreEdges = 0
	for e in coreEdges:
		sum = sum + costDic[tuple(e)]
		numberOfCoreEdges = numberOfCoreEdges + 1
	splitterCosts = (sum/numberOfCoreEdges)/2
	
	for e in coreEdges:
		flag = False
		for c in cos:
			if e[2] == c[1]:
				flag = True
		if not flag:
			edges.append([e[0], e[1] + '_reverse', e[3], e[2], e[4], e[5]])
			costDic[e[0], e[1] + '_reverse', e[3], e[2], e[4], e[5]] = costDic[tuple(e)]
	
	dataDic['edges'] = edges
	nodes = dataDic['nodes']
	
	facilitys, steinerNodes, cos, customers, coreEdges, assEdges1, assEdges2 = datanice.datanice(dataDic)
	
	facilitys1=[]
	facilitys2=[]
	#need the following only for debugging
	#facilitiesOnlyNames1 = []
	#facilitiesOnlyNames2 = []
	#customersOnlyNames = []
	for f in facilitys:
		if f[5]==1:
			facilitys1.append(f)
	#		facilitiesOnlyNames1.append(f[1])
		else:
			facilitys2.append(f)
	#		facilitiesOnlyNames2.append(f[1])
	#
	#for cust in customers:
	#	customersOnlyNames.append(cust[1])	
	
	
	min_root = None
	min_costs = None

	
	for e in edges:
		if e[0] == 'assEdge1':
			costDic[tuple(e)] = costDic[tuple(e)] - period * profitDic[e[3]][0]
		if e[0] == 'assEdge2':
			costDic[tuple(e)] = costDic[tuple(e)] - period * profitDic[e[3]][1]
	
	
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
		
		edgeNumberDic={}
		for e in solutionModel:
			edgeNumberDic[e[2],e[3]]=x[e[2],e[3]].X
		
		
		
		costsfinal = model.ObjVal + costDic[root[1]]
		
		if min_costs == None or costsfinal < min_costs:
			min_costs = costsfinal
			min_root = root
			min_solution = solutionModel
			minEdgeNumberDic = edgeNumberDic
			min_s = s
			min_m = m

	nCustsAssignedByFiber = 0
	for e in min_solution:
		if e[0] == 'assEdge1':
			nCustsAssignedByFiber = nCustsAssignedByFiber + 1

	return facilitys,steinerNodes,cos,customers,coreEdges,assEdges1,assEdges2,min_costs,min_root,min_solution,minEdgeNumberDic,nCustsAssignedByFiber,min_m,min_s



instance = 'b'
splittingNumber = 4
plotEdgeNumbers = False
timelimit = 7200

demandAndPeriodList = []
paramList = []
for dmdFac in [1]: #, 1.5, 2, 2.5, 3,3.5,4,4.5,5]:
	for per in [0]:  #, 12*10, 12*20]:
		paramList.append([dmdFac, per])

for [demandFactor, period] in paramList:
	start_time = time.time()
	facilitys,steinerNodes,cos,customers,coreEdges,assEdges1,assEdges2,min_costs,min_root,min_solution,minEdgeNumberDic,nCustsAssignedByFiber,m,s=solve_p2mp(instance,demandFactor,period, splittingNumber, timelimit)
	
	demandAndPeriodList.append([demandFactor, period, min_root[1], min_costs, nCustsAssignedByFiber])
	
	elapsed_time = time.time() - start_time
	
	print("time: ", elapsed_time, "s")

	plotSolution.plotSolution(facilitys,steinerNodes,cos,customers,min_solution,min_root,minEdgeNumberDic,m,s,False,plotEdgeNumbers)

print("\n", demandAndPeriodList, "\n")
