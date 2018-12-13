import readWrite
import preprocess
import solveOnlyFiber
import time

start_time = time.time()

dataDic, costDic, profitDic = readWrite.read('v')

dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic, 1)

dijkList = []

facAndSteinerNodes = []
facAndSteinerEdges = []


for node in dataDic['nodes']:
	if node[0] in ['facility', 'steiner', 'co']:
		facAndSteinerNodes.append(node)

for edge in dataDic['edges']:
	if edge[0] == 'coreEdge':
		facAndSteinerEdges.append(edge)

for co in dataDic['CONodes']:
	coDuplicate = ['co'] + [co[0], co[1], co[2]]
	if not facAndSteinerNodes[0] == coDuplicate:
		facAndSteinerNodes.remove(coDuplicate)
		facAndSteinerNodes.insert(0, coDuplicate)
	
	vis, pa = preprocess.dijkstra(facAndSteinerNodes, facAndSteinerEdges, co[0], costDic)
	dijkList.append([co[0], vis])


min_root, min_cost, predec, solution = solveOnlyFiber.solveOnlyFiber(dataDic, dijkList, costDic)



print("min_co: ", min_root, " min_cost: ", min_cost)

elapsed_time = time.time() - start_time

print("time: ", elapsed_time, "s")