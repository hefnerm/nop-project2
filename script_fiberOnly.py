import readWrite
import preprocess
import graphalgs
import datanice
import solveOnlyFiber
import plotSolution
import time

instance = 'v'    #Choose between n (Naunyn), b (Berlin), v (Vehlefanz)
demandFactor = 1    # will multiply the demand (if you want to suppose that the demand increases) 
					#does not matter here, because fiber has capacity infintely
plotEdgeNumbers = False #Choose between False (no Numbers on the Edges in the plot) or True ( plot Numbers on the Edges in the plot)

start_time = time.time()

dataDic, costDic, profitDic = readWrite.read(instance)

dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic, demandFactor)

facilities, steinerNodes, cos, customers, coreEdges, assEdges1, assEdges2 = datanice.datanice(dataDic)

dijkList = []

facAndSteinerNodes = []
facAndSteinerEdges = []
numberEdgeInTree = {}


#for node in dataDic['nodes']:
#	if node[0] in ['facility', 'steiner', 'co']:
#		facAndSteinerNodes.append(node)

#for edge in dataDic['edges']:
#	if edge[0] == 'coreEdge':
#		facAndSteinerEdges.append(edge)

#for co in dataDic['CONodes']:
#	coDuplicate = ['co'] + [co[0], co[1], co[2]]
#	if not facAndSteinerNodes[0] == coDuplicate:
#		facAndSteinerNodes.remove(coDuplicate)
#		facAndSteinerNodes.insert(0, coDuplicate)
#	
#	vis, pa = preprocess.dijkstra(facAndSteinerNodes, facAndSteinerEdges, co[0], costDic)
#	dijkList.append([co[0], vis])

nodes = cos + facilities + steinerNodes

for co in cos:
	if not co == nodes[0]:
		nodes.remove(co)
		nodes.insert(0, co)
	
	vis, pa = preprocess.dijkstra2(nodes, coreEdges, co[1], costDic)
	dijkList.append([co[1], vis, pa])

min_root, min_cost, predec, solutionEdges = solveOnlyFiber.solveOnlyFiber(dataDic, facilities, customers, assEdges1, dijkList, costDic)

#print("solution: ", solution)

dijkstraListToExtract = None

for nodeDijk in dijkList:
	if min_root == nodeDijk[0]:
		dijkstraListToExtract = nodeDijk[2]
		break


for cust in customers:
	#path = graphalgs.getPathP2MP(coreEdges, min_root, predec[cust[1]])
	#path = graphalgs.getPathFromDijkstra(coreEdges, min_root, predec[cust[1]])
	path, length = preprocess.getPathEdgesDij(min_root, predec[cust[1]], dijkstraListToExtract, coreEdges)
	#print("path: ", path)
	solutionEdges = solutionEdges + path

for e in coreEdges + assEdges1 + assEdges2:
	num = solutionEdges.count(e)
	if num > 0:
		numberEdgeInTree[e[2],e[3]] = num

#print(numberEdgeInTree)

print("min_co: ", min_root, " min_cost: ", min_cost)

elapsed_time = time.time() - start_time

print("time: ", elapsed_time, "s")

min_root=[0,min_root]

plotSolution.plotSolution(facilities, steinerNodes, cos, customers, solutionEdges, min_root,numberEdgeInTree,None,None,True,plotEdgeNumbers)
