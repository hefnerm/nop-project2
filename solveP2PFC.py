import steinerflowmodel
import preprocess
import datanice
import readWrite
#import plotSolution
import time

#parameter to solve the P2PFC
instance = 'v'     # Choose between n (Naunyn), b (Berlin), v (Vehlefanz)
demandFactor =  1 	# will multiply the demand (if you want to suppose that the demand increases)

period = 12*10  	#to calculate profit you can here choose for how many years you want to plan
plotEdgeNumbers=False   #Choose between False (no Numbers on the Edges in the plot) or True ( plot Numbers on the Edges in the plot)

#read the data
dataDic, costDic, profitDic = readWrite.read(instance)

#preprocess the data, so that the customers demand is statisfied for any network in this graph
dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic, demandFactor)

#splitt the data in comfortable sets
facilitys, steinerNodes, cos, customers, coreEdges, assEdges1, assEdges2 = datanice.datanice(dataDic)

min_root = None
min_costs = None

start_time = time.time()

solution = {}

# for every root we calculate a mincost network
for root in cos:
	#model the first helping grpah
	nodesDij = [root] + steinerNodes + facilitys
	if not nodesDij[0] == root:
		nodesDij.remove(root)
		nodesDij.insert(0, root)

	#solve dijkstra in this graph
	vis, pa = preprocess.dijkstra(nodesDij, coreEdges, root[1], costDic)
	#make the second helping graph
	nodesModel = facilitys + customers + [root]
	edgesModel = assEdges1 + assEdges2
	
	for n in facilitys:
		e = ['shortestpath', 'sp_' + root[1] + '_' + n[1] , root[1], n[1]]
		edgesModel.append(e)
	
	#make the costfunction c'
	costsModel = {}
	for n in facilitys:
		if n[5] == 2:
			costsModel[root[1], n[1]] = vis[n[1]] + costDic[n[1]]
		if n[5] == 1:
			costsModel[root[1], n[1]] = vis[n[1]]
	for e in assEdges1:
		costsModel[e[2], e[3]] = costDic[tuple(e)] + costDic[e[2]] - period * profitDic[e[3]][0]
	for e in assEdges2:
		costsModel[e[2], e[3]] = costDic[tuple(e)] - period * profitDic[e[3]][1]

	#solve the steinertree model with the flow formulation on the second helping graph
	model, solutionModel = steinerflowmodel.solve_steinerflowmodel(nodesModel, customers, root, edgesModel, costsModel)
	
	#final costs are the costs from the solution plus the co building costs
	costsfinal = model.ObjVal + costDic[root[1]]
	
	#search for the cheapest co
	if min_costs == None or min_costs > costsfinal:
		min_costs = costsfinal
		min_root = root
	
	#make the complete solution out of the two solutions from the two graphs
	solution[root[1]]=[]
	for e in solutionModel:
		if e[0] == 'shortestpath':
			path, length = preprocess.getPathEdgesDij(e[2],e[3],pa,coreEdges)
			for pathEdge in path:
				if not pathEdge in solution[root[1]]:
					solution[root[1]].append(pathEdge)
		else:
			solution[root[1]].append(e)

#how much fiber assignments are in the solution?
numberFiberAss = 0
for e in solution[min_root[1]]:
	if e[0] == 'assEdge1':
		numberFiberAss = numberFiberAss+1

#print everything
print("min_co: ", min_root[1], " min_costs: ", min_costs, 'number of fiber assignments:',numberFiberAss)

elapsed_time = time.time() - start_time
print("time: ", elapsed_time, "s")

#plot the solution
numberEdgeInTree = {}
for e in coreEdges + assEdges1 + assEdges2:

	num = solution[min_root[1]].count(e)
	if num > 0:
		numberEdgeInTree[e[2],e[3]] = num

#plotSolution.plotSolution(facilitys, steinerNodes, cos, customers, solution[min_root[1]], min_root,numberEdgeInTree,None,None,True,plotEdgeNumbers)
