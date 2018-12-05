import matplotlib.pyplot as plt

def plotSolution(facilitys, steinerNodes, cos, customers, solutionEdges, solutionRoot):
	
	ax = plt.axes()
	ax.axis('off')
	
	coordFacilitysX = []
	coordFacilitysY = []
	coordXDic = {}
	coordYDic = {}
	color = []
	for n in facilitys:
		coordFacilitysX.append(n[2])
		coordFacilitysY.append(n[3])
		coordXDic[n[1]] = n[2]
		coordYDic[n[1]] = n[3]
		flag = False
		for e in solutionEdges:
			if n[1] == e[2] or n[1] == e[3]:
				flag = True
		if flag:
			color.append('blue')
		else:
			color.append('#1aa3ff')
	ax.scatter(coordFacilitysX, coordFacilitysY, s = 10, c = color, label = 'Facility nodes', zorder = 2)
	
	coordCosX = []
	coordCosY = []
	
	color = []
	
	#undo change: changed list where to run over from cos to [solutionRoot]
	for n in [solutionRoot]:
		coordCosX.append(n[2])
		coordCosY.append(n[3])
		coordXDic[n[1]] = n[2]
		coordYDic[n[1]] = n[3]
		if n[1] == solutionRoot[1]:
			color.append('red')
		else:
			raise Exception("shouldnt do this in test; undo change a few lines ago and delete this exception")
			color.append('#E80000')
	ax.scatter(coordCosX, coordCosY, s = 10, c = color, label = 'CO nodes', zorder = 2)
	
	coordSteinerX = []
	coordSteinerY = []
	color = []
	
	for n in steinerNodes:
		#steinerNodeHasOutgoingEdge = False
		#steinerNodeHasIncomingEdge = False
		#for edge in solutionEdges:
		#	if edge[2] == n[1]:
		#		steinerNodeHasOutgoingEdge = True
		#	if edge[3] == n[1]:
		#		if steinerNodeHasIncomingEdge:
		#			raise Exception("steiner node has multiple incoming edges")
		#		steinerNodeHasIncomingEdge = True
		#
		#if steinerNodeHasOutgoingEdge != steinerNodeHasIncomingEdge:
		#	print(n)
		#	print("hasOutgoing: ", steinerNodeHasOutgoingEdge)
		#	raise Exception("steiner node hasIncoming != hasOutgoing")
		#if not (steinerNodeHasIncomingEdge and steinerNodeHasOutgoingEdge):
		#	continue
		
		coordSteinerX.append(n[2])
		coordSteinerY.append(n[3])
		coordXDic[n[1]] = n[2]
		coordYDic[n[1]] = n[3]
		color.append('green')
		ax.scatter(coordSteinerX, coordSteinerY, s = 10, c = color, label = 'Steiner nodes', zorder = 2)
	
	coordCustomersX = []
	coordCustomersY = []
	coordCustomerXDic = {}
	coordCustomerYDic = {}
	color = []
	for n in customers:
		coordCustomersX.append(n[2] + 0.0002)
		coordCustomersY.append(n[3] + 0.0002)
		coordXDic[n[1]] = n[2] + 0.0002
		coordYDic[n[1]] = n[3] + 0.0002
		color.append('yellow')
	ax.scatter(coordCustomersX, coordCustomersY, s = 10, c = color, label = 'Customer nodes (next to corresponding facility node)', zorder = 2)

	for e in solutionEdges:
		ax.arrow(coordXDic[e[2]], coordYDic[e[2]] , coordXDic[e[3]] - coordXDic[e[2]], coordYDic[e[3]] - coordYDic[e[2]], fc = "k", ec= "k", head_width = 0, head_length = 0, width = 0.00001)
	
	#ax.legend()
	plt.show()