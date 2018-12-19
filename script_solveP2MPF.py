import readWrite
import p2mpModelF
import datanice
import preprocess
import plotSolution
import time

#######parameters you can change
instance = 'n'     #chooose from 'n' (Naunyn), 'b' (Berlin), 'v' (Vehlefanz)
demandFactor = 1    # dont need to be increase here because fiber has ininite capacity
splittingNumber = 4   # in how much kables can one splitter split one kabel, choose between 4 or 16
plotEdgeNumbers = False  #Choose between False (no Numbers on the Edges in the plot) or True ( plot Numbers on the Edges in the plot)
timelimit = 7200           #Timelimit for gurobi 
############################
start_time = time.time()

dataDic, costDic, profitDic = readWrite.read(instance)
dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic, demandFactor)

nodes = dataDic['nodes']
edges = dataDic['edges']
facilities, steinerNodes, cos, customers, coreEdges, assEdges1, assEdges2 = datanice.datanice(dataDic)

#splitter costs calculation
sum = 0
nOfCoreEdges = 0
for e in coreEdges:
	sum = sum + costDic[tuple(e)]
	nOfCoreEdges = nOfCoreEdges + 1
splitterCosts = (sum/nOfCoreEdges)/2

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

#update the edges
dataDic['edges'] = edges
facilities, steinerNodes, cos, customers, coreEdges, assEdges1, assEdges2 = datanice.datanice(dataDic)

min_root = None
min_costs = None
min_ub = None
best_lb_costs = None
solutionIsUpperBound = None


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
	model, x, y, s, solutionModel = p2mpModelF.solve_P2MPModelFiber(nodes, coreEdgesNew + assEdges1, root, cos, facilities, customers, steinerNodes, coreEdges, costDic, splittingNumber, splitterCosts, timelimit)
	
	if model.status == 2:
		edgeNumberDic = {}
		for e in solutionModel:
			edgeNumberDic[e[2], e[3]] = x[e[2], e[3]].X
		
		costsfinal = model.ObjVal + costDic[root[1]]
	#find the best solution
		if min_costs == None or costsfinal < min_costs:
			min_costs = costsfinal
			min_root = root
			min_solution = solutionModel
			minEdgeNumberDic = edgeNumberDic
			min_s = s
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
			best_lb_costs = model.ObjBound + costDic[root[1]]
			solutionIsUpperBound = True

if solutionIsUpperBound:
	print("solution is only an upper bound!")
print("min_co: ", min_root[1], " costs: ", min_costs)

elapsed_time = time.time() - start_time

print("time: ", elapsed_time, "s")

m = {}
for f in facilities:
	if f[5] == 2:
		m[f[1]] = 0

plotSolution.plotSolution(facilities, steinerNodes, cos, customers, min_solution, min_root, minEdgeNumberDic, m, min_s, False, plotEdgeNumbers)


