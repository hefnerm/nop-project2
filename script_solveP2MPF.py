import readWrite
import p2mpModelF
import datanice
import preprocess
import plotSolution
import time

instance = 'v'
demandFactor = 1
splittingNumber = 4
timelimit = 1000000000000

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

for e in coreEdges:
	flag = False
	for c in cos:
		if e[2] == c[1]:
			flag = True 
	if not flag:
		edges.append([e[0], e[1], e[3], e[2], e[4], e[5]])
		costDic[e[0], e[1], e[3], e[2], e[4], e[5]] = costDic[tuple(e)]

dataDic['edges'] = edges
facilities, steinerNodes, cos, customers, coreEdges, assEdges1, assEdges2 = datanice.datanice(dataDic)

min_root = None
min_costs = None


for e in edges:
	if e[0] == 'assEdge1':
		costDic[tuple(e)] = costDic[tuple(e)]

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
	
	model, x, y, s, solutionModel = p2mpModelF.solve_P2MPModelFiber(nodes, coreEdges+assEdges1, root, cos, facilities, customers, steinerNodes, coreEdges, costDic, splittingNumber, splitterCosts, timelimit)
	
	edgeNumberDic = {}
	for e in solutionModel:
		edgeNumberDic[e[2],e[3]] = x[e[2],e[3]].X
	
	
	costsfinal = model.ObjVal + costDic[root[1]]
	
	if min_costs == None or costsfinal < min_costs:
		min_costs = costsfinal
		min_root = root
		min_solution = solutionModel
		minEdgeNumberDic = edgeNumberDic
		min_s=s
	
print("min_co: ", min_root[1], " costs: ", min_costs)

elapsed_time = time.time() - start_time

print("time: ", elapsed_time, "s")

m={}
for f in facilities:
	if f[5]==2:
		m[f[1]]=0

plotSolution.plotSolution(facilities,steinerNodes,cos,customers,min_solution,min_root,minEdgeNumberDic,m,s,False,True)


