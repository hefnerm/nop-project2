import readWrite
import preprocess
import graphalgs
import datanice
import solveOnlyFiber
import plotSolution
import time

instance = 'n'    #Choose between n (Naunyn), b (Berlin), v (Vehlefanz)
demandFactor = 1    # will multiply the demand (if you want to suppose that the demand increases) 
					#does not matter here, because fiber has capacity infintely
plotEdgeNumbers = True #Choose between False (no Numbers on the Edges in the plot) or True ( plot Numbers on the Edges in the plot)

start_time = time.time()

#read the instance
dataDic, costDic, profitDic = readWrite.read(instance)
#preprocess, so the demand is satisfied
dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic, demandFactor)

facilities, steinerNodes, cos, customers, coreEdges, assEdges1, assEdges2 = datanice.datanice(dataDic)

#construct helping graph
dijkList = []

facAndSteinerNodes = []
facAndSteinerEdges = []
numberEdgeInTree = {}

nodes = cos + facilities + steinerNodes
#dijkstra for every co on the graph (edges=coreedges)
for co in cos:
	
	#ensure that the root is at the first place of the list
	if not co == nodes[0]:
		nodes.remove(co)
		nodes.insert(0, co)
	
	vis, pa = preprocess.dijkstra2(nodes, coreEdges, co[1], costDic)
	dijkList.append([co[1], vis, pa])

#gives the min_root and the min_costs and the solution edges
min_root, min_cost, predec, solutionEdges = solveOnlyFiber.solveOnlyFiber(dataDic, facilities, customers, assEdges1, dijkList, costDic)

dijkstraListToExtract = None

for nodeDijk in dijkList:
	if min_root == nodeDijk[0]:
		dijkstraListToExtract = nodeDijk[2]
		break

#construct the edges of the path for every customer
for cust in customers:
	path, length = preprocess.getPathEdgesDij(min_root, predec[cust[1]], dijkstraListToExtract, coreEdges)
	solutionEdges = solutionEdges + path

for e in coreEdges + assEdges1 + assEdges2:
	num = solutionEdges.count(e)
	if num > 0:
		numberEdgeInTree[e[2],e[3]] = num

print("min_co: ", min_root, " min_cost: ", min_cost)

elapsed_time = time.time() - start_time

print("time: ", elapsed_time, "s")

min_root = [0, min_root]

plotSolution.plotSolution(facilities, steinerNodes, cos, customers, solutionEdges, min_root, numberEdgeInTree, None, None, True, plotEdgeNumbers)
