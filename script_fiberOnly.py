import readWrite
import preprocess
import solveOnlyFiber
import time

start_time = time.time()

dataDic, costDic = readWrite.read('v')

dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic)

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
	

min_root, min_cost, predec = solveOnlyFiber.solveOnlyFiber(dataDic, dijkList, costDic)

print("\nmin_root: ", min_root)
print("\nmin_cost: ", min_cost)
#print("\npredec: ",predec)

elapsed_time = time.time() - start_time

print("time: ", elapsed_time)