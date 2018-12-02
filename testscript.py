import readWrite
import preprocess

dataDic, costDic = readWrite.read('n')

dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic)

print(dataDic)