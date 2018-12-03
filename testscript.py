import readWrite
import preprocess

dataDic, costDic = readWrite.read('n')

dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic)



vis, pa = preprocess.dijkstra(dataDic['nodes'], dataDic['edges'], dataDic['CONodes'][0], costDic)

print("visited: ", vis)
print("\n\npath: ", pa)