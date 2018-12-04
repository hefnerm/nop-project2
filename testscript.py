import readWrite
import preprocess
import datanice

dataDic, costDic = readWrite.read('n')

dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic)
facilitys,steinerNodes,cos,customers,coreEdges,assEdges1,assEdges2=datanice.datanice(dataDic)

nodesDij=cos+steinerNodes+facilitys

vis, pa = preprocess.dijkstra(nodesDij, coreEdges, cos[0], costDic)



path=preprocess.getPathEdgesDij(cos[0][1],facilitys[3][1],pa,coreEdges)

print("visited: ", vis)
print("\n\npath: ", pa)
print('\n',cos[0][1],'\n',facilitys[3][1],'\n',path)