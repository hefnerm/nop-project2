import preprocess
import datanice
import readWrite
import plotSolution
import p2mpmodel
import graphalgs
import time

#imput: instance: name of type 'n', 'b', 'v'; demandFactor: the factor the demand of each customer has changed; period: the number of months the profits shall be considered; splittingNumber: the number of fiber edges a splitter can split up to, 1 gives the P2P solution; timelimit
#output: facilities, steinerNodes, cos, customers: all nodes; coreEdges, assEdges1, assEdges2: all edges; min_costs, min_root, min_solution, minEdgeNumberDic, nCustsAssignedByFiber, min_m, min_s, solutionIsUpperBound: solution parameters
def solve_p2mp(instance, demandFactor, period, splittingNumber, timelimit):
	
	dataDic, costDic, profitDic = readWrite.read(instance)
	dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic, demandFactor)
	
	edges = dataDic['edges']

	facilities, steinerNodes, cos, customers, coreEdges, assEdges1, assEdges2 = datanice.datanice(dataDic)

	#splittercosts calculation
	sum = 0
	numberOfCoreEdges = 0
	for e in coreEdges:
		sum = sum + costDic[tuple(e)]
		numberOfCoreEdges = numberOfCoreEdges + 1
	splitterCosts = (sum/numberOfCoreEdges)/2
	
	#add all reversed inner core edges because we consider these edges as undirected
	for e in coreEdges:
		flag = False
		
		#but not the edges coming from a co, they can only be used from the co and not to the co
		for c in cos:
			if e[2] == c[1]:
				flag = True
		if not flag:
			edges.append([e[0], e[1] + '_reverse', e[3], e[2], e[4], e[5]])
			costDic[e[0], e[1] + '_reverse', e[3], e[2], e[4], e[5]] = costDic[tuple(e)]
	
	#update the data
	dataDic['edges'] = edges
	nodes = dataDic['nodes']
	
	facilities, steinerNodes, cos, customers, coreEdges, assEdges1, assEdges2 = datanice.datanice(dataDic)
	
	facilities1 = []
	facilities2 = []
	for f in facilities:
		if f[5] == 1:
			facilities1.append(f)
		else:
			facilities2.append(f)
	
	
	min_root = None
	min_costs = None
	
	best_ub = None
	best_ub_costs = None
	best_lb_costs = None
	solutionIsUpperBound = None
	
	#adjust the costs of an assignment edge in case of considering profits (otherwise period = 0)
	for e in edges:
		if e[0] == 'assEdge1':
			costDic[tuple(e)] = costDic[tuple(e)] - period * profitDic[e[3]][0]
		if e[0] == 'assEdge2':
			costDic[tuple(e)] = costDic[tuple(e)] - period * profitDic[e[3]][1]
	
	
	for root in cos:
		#create a new list of core edges without the edges from the other cos, which are not considered right now
		coreEdgesNew = []
		for e in coreEdges:
			flag = False
			for c in cos:
				if c[1] != root[1]:
					if (e[2] == c[1]):
						flag = True
			if not flag:
				coreEdgesNew.append(e)
		
		#solve the model
		model, x, y, s, m, solutionModel = p2mpmodel.solve_P2MPModel(nodes, edges, root, cos, facilities, facilities1, facilities2, customers, steinerNodes, coreEdgesNew, assEdges1, assEdges2, costDic, splittingNumber, splitterCosts, timelimit)
		
		if model.status == 2:
			edgeNumberDic = {}
			for e in solutionModel:
				edgeNumberDic[e[2], e[3]] = x[e[2], e[3]].X
			
			costsfinal = model.ObjVal + costDic[root[1]]
			
			if min_costs == None or costsfinal < min_costs:
				min_costs = costsfinal
				min_root = root
				min_solution = solutionModel
				minEdgeNumberDic = edgeNumberDic
				min_s = s
				min_m = m
				best_lb_costs = None
				solutionIsUpperBound = False
		
		#in this case the model only returned an upper bound
		elif model.status in [9, 11]:
			edgeNumberDic = {}
			for e in solutionModel:
				edgeNumberDic[e[2], e[3]] = x[e[2], e[3]].ub
			
			costsfinal = model.ObjVal + costDic[root[1]]
			
			if min_costs == None or costsfinal < min_costs:
				min_costs = costsfinal
				min_root = root
				min_solution = solutionModel
				minEdgeNumberDic = edgeNumberDic
				min_s = s
				min_m = m
				best_lb_costs = model.ObjBound + costDic[root[1]]
				solutionIsUpperBound = True
	
	nCustsAssignedByFiber = 0
	for e in min_solution:
		if e[0] == 'assEdge1':
			nCustsAssignedByFiber = nCustsAssignedByFiber + 1
	
	return facilities, steinerNodes, cos, customers, coreEdges, assEdges1, assEdges2, min_costs, min_root, min_solution, minEdgeNumberDic, nCustsAssignedByFiber, min_m, min_s, solutionIsUpperBound



instance = 'v'
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
	facilities, steinerNodes, cos, customers, coreEdges, assEdges1, assEdges2, min_costs, min_root, min_solution, minEdgeNumberDic, nCustsAssignedByFiber, m, s, isUpperBound = solve_p2mp(instance, demandFactor, period, splittingNumber, timelimit)
	
	demandAndPeriodList.append([demandFactor, period, min_root[1], min_costs, nCustsAssignedByFiber, isUpperBound])
	elapsed_time = time.time() - start_time
	if isUpperBound:
		print("solution is only an upper bound!")
		print("best lower bound: ", best_lb_costs)
	print("time: ", elapsed_time, "s")

	plotSolution.plotSolution(facilities, steinerNodes, cos, customers, min_solution, min_root, minEdgeNumberDic, m, s, False, plotEdgeNumbers)

print("\n", demandAndPeriodList, "\n")
