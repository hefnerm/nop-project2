import readWrite
import preprocess
import solveOnlyFiber
import time
import datanice

start_time = time.time()

dataDic, costDic = readWrite.read('v')

print(len(dataDic['AssEdges2']))

dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic, 1)

print(len(dataDic['AssEdges2']))

