import preprocess
import datanice
import readWrite
import plotSolution
import p2mptest
import graphalgs


dataDic, costDic = readWrite.read('b')
dataDic = preprocess.deleteAssEdgesP2P(dataDic, costDic, 1)

edges=dataDic['edges']
facilitys,steinerNodes,cos,customers,coreEdges,assEdges1,assEdges2=datanice.datanice(dataDic)


for e in coreEdges:
	if e[2] != cos[0][1]:
		edges.append([e[0],e[1],e[3],e[2],e[4],e[5]])
		costDic[e[0],e[1],e[3],e[2],e[4],e[5]]=costDic[tuple(e)]


facilitys1=[]
facilitys2=[]
for f in facilitys:
	if f[5]==1:
		facilitys1.append(f)
	else:
		facilitys2.append(f)

maxi=0
temp=0
for f in facilitys:
	for e in assEdges2:
		if f[1]==e[2]:
			temp=temp+1
	if maxi<temp:
		maxi=temp
	temp=0

############################splitngnumber=1 sollte lösung für p2p ergeben. tuts aber leider nicht :(#####################################
splittingNumber=1

summ=0
numberOfCoreEdges=0
for e in coreEdges:
	summ=summ+costDic[tuple(e)]
	numberOfCoreEdges=numberOfCoreEdges+1
splitterCosts=(summ/numberOfCoreEdges)/2
#print(splitterCosts)

#print(costDic)
print("root included: ",cos[0] in facilitys+steinerNodes+customers)
nodes = cos + facilitys + steinerNodes + customers
for root in [cos[0]]:
	#nodes=[root]+facilitys+steinerNodes+customers
	model,x,y,solution=p2mptest.solve_P2MPModel(nodes,edges,root,facilitys,facilitys1,facilitys2,customers,steinerNodes,coreEdges,assEdges1,assEdges2,costDic,maxi,splittingNumber,splitterCosts)
	
	costsfinal=model.ObjVal+costDic[root[1]]
	print(root[1], " : ", costsfinal)
	
	for t in customers:
		solutionCust = []
		for e in edges:
			if y[e[2],e[3],t[1]].X>0.5:
				solutionCust.append(e)
		plotSolution.plotSolution(facilitys,steinerNodes,cos,customers,solutionCust,root)

nCustWRootConnection = 0
nCustWORootConnection = 0
for t in customers:
	#if t[1] != 'B_553_cust':
		path = graphalgs.getPathP2MP(solution, root, t)
		if path == -1:
			nCustWORootConnection = nCustWORootConnection + 1
		else:
			print("cust ", t, " has connection to root")
			nCustWRootConnection = nCustWRootConnection + 1

print("nCustWOCon: ", nCustWORootConnection)
print("nCustWCon: ", nCustWRootConnection)



