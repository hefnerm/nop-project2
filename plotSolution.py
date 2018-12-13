import matplotlib.pyplot as plt

def plotSolution(facilitys, steinerNodes, cos, customers, solutionEdges, solutionRoot):
	
	ax = plt.axes()
	ax.axis('off')
	

	coordXDic = {}
	coordYDic = {}


	coordCosX = []
	coordCosY = []
	
	color = []

	#undo change: changed list where to run over from cos to [solutionRoot]
	for n in cos:
		coordCosX.append(n[2])
		coordCosY.append(n[3])
		coordXDic[n[1]] = n[2]
		coordYDic[n[1]] = n[3]
		if n[1] == solutionRoot[1]:
			color.append('red')
		else:
			#raise Exception("shouldnt do this in test; undo change a few lines ago and delete this exception")
			color.append('#ff4d4d')
	axl=ax.scatter(coordCosX, coordCosY,marker='s', s = 10, c = color, label = 'Leitstellen', zorder = 2)
	
	coordFacilitysX = []
	coordFacilitysY = []
	
	color=[]

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
	axf=ax.scatter(coordFacilitysX, coordFacilitysY, s = 10, c = color, label = 'Facilitys', zorder = 2)
	
	
	coordSteinerX = []
	coordSteinerY = []
	color = []
	
	for n in steinerNodes:
		coordSteinerX.append(n[2])
		coordSteinerY.append(n[3])
		coordXDic[n[1]] = n[2]
		coordYDic[n[1]] = n[3]
		color.append('green')
	axs=ax.scatter(coordSteinerX, coordSteinerY, s = 10, c = color, label = 'Steiner Knoten', zorder = 2)
	
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
	axk=ax.scatter(coordCustomersX, coordCustomersY, marker='^', s = 10, c = color, label = 'Kunden (leicht versetzt)', zorder = 2)
	
	for e in solutionEdges:
		if e[0]=='assEdge1':
			ax.arrow(coordXDic[e[2]], coordYDic[e[2]] , coordXDic[e[3]] - coordXDic[e[2]], coordYDic[e[3]] - coordYDic[e[2]], fc = "#00ff00" , ec = '#00ff00', head_width = 0, head_length = 0, width = 0.00001 , label='Anschlusskanten 1')
		elif e[0]=='assEdge2':
			ax.arrow(coordXDic[e[2]], coordYDic[e[2]] , coordXDic[e[3]] - coordXDic[e[2]], coordYDic[e[3]] - coordYDic[e[2]], fc = '#ff0066', ec = "#ff0066", head_width = 0, head_length = 0, width = 0.00001, label='Anschlusskanten 2')
		elif e[0]=='coreEdge':
			ax.arrow(coordXDic[e[2]], coordYDic[e[2]] , coordXDic[e[3]] - coordXDic[e[2]], coordYDic[e[3]] - coordYDic[e[2]], fc = "k", ec = "k", head_width = 0, head_length = 0, width = 0.00001, label='innere Kanten')


#fontsize : int or float or {'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'}
	ax.legend(fontsize='xx-small')
	dlinex1, = plt.plot([],[],color="#00ff00", linewidth=1)
	dlinex2, = plt.plot([],[],color='#ff0066', linewidth=1)
	dlinexc, = plt.plot([],[],color="k", linewidth=1)

	ax.legend([axl,axf,axs,axk,dlinexc,dlinex1,dlinex2],['Leitstellen','Facilitys','Steinerknoten','Kunden (leicht versetzt)','innere Kanten','Anschlusskanten Glasfaser','Anschlusskanten Kupfer'],fontsize='xx-small')
	plt.show()
	#plt.savefig('test.png')                        


