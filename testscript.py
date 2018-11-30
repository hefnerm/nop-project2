import readWrite
import preprocess

dataDic, costDic = readWrite.read('b')

dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic)
