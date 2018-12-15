import matplotlib.pyplot as plt

def plotSolution(facilitys, steinerNodes, cos, customers, solutionEdges, solutionRoot,numberDic,m,s,P2P):
	
	ax=plt
	ax.axis('off')

	coordXDic = {}
	coordYDic = {}

	coordCosX = []
	coordCosY = []
	color = []

	for n in cos:
		coordCosX.append(n[2])
		coordCosY.append(n[3])
		coordXDic[n[1]] = n[2]
		coordYDic[n[1]] = n[3]
		if n[1] == solutionRoot[1]:
			color.append('red')
		else:
			color.append('#ff4d4d')
	axl=ax.scatter(coordCosX, coordCosY,marker='s', s = 10, c = color, label = 'Leitstellen', zorder = 3)
	
###################################################
	coordFacilitysX1 = []
	coordFacilitysY1 = []
	coordFacilitysX2 = []
	coordFacilitysY2 = []
	
	color1 = []
	color2 = []


	if P2P:
		for n in facilitys:
			coordXDic[n[1]] = n[2]
			coordYDic[n[1]] = n[3]
			coordFacilitysX1.append(n[2])
			coordFacilitysY1.append(n[3])

			flag = False
			for e in solutionEdges:
				if n[1] == e[2] or n[1] == e[3]:
					flag = True
			if flag:
				color1.append('blue')
			else:
				color1.append('#1aa3ff')
		axf=ax.scatter(coordFacilitysX1, coordFacilitysY1, s = 10, c = color1, label = 'Facilitys', zorder = 3)
	else:
		for n in facilitys:
			coordXDic[n[1]] = n[2]
			coordYDic[n[1]] = n[3]

			if n[5]==2:
				if m[n[1]].X>0.5:
					coordFacilitysX1.append(n[2])
					coordFacilitysY1.append(n[3])
					flag = False
					for e in solutionEdges:
						if n[1] == e[2] or n[1] == e[3]:
							flag = True
					if flag:
						color1.append('blue')
					else:
						color1.append('#1aa3ff')
				elif s[n[1]].X>0.5:
					coordFacilitysX1.append(n[2])
					coordFacilitysY1.append(n[3])
					flag = False
					for e in solutionEdges:
						if n[1] == e[2] or n[1] == e[3]:
							flag = True
					if flag:
						color1.append('blue')
					else:
						color1.append('#1aa3ff')
				else:
					coordFacilitysX2.append(n[2])
					coordFacilitysY2.append(n[3])
					flag = False
					for e in solutionEdges:
						if n[1] == e[2] or n[1] == e[3]:
							flag = True
					if flag:
						color2.append('blue')
					else:
						color2.append('#1aa3ff')
			else:
				if s[n[1]].X>0.5:
					coordFacilitysX1.append(n[2])
					coordFacilitysY1.append(n[3])
					flag = False
					for e in solutionEdges:
						if n[1] == e[2] or n[1] == e[3]:
							flag = True
					if flag:
						color1.append('blue')
					else:
						color1.append('#1aa3ff')
				else:
					coordFacilitysX2.append(n[2])
					coordFacilitysY2.append(n[3])
					flag = False
					for e in solutionEdges:
						if n[1] == e[2] or n[1] == e[3]:
							flag = True
					if flag:
						color2.append('blue')
					else:
						color2.append('#1aa3ff')

		axf1=ax.scatter(coordFacilitysX1, coordFacilitysY1, s = 10, c = color1, marker='*', label = 'Facilitys', zorder = 3)
		axf2=ax.scatter(coordFacilitysX2, coordFacilitysY2, s = 10, c = color2, marker='o', label = 'Facilitys', zorder = 3)

########################################	
	coordSteinerX1 = []
	coordSteinerY1 = []
	coordSteinerX2 = []
	coordSteinerY2 = []
	color1 = []
	color2 = []
	
	if P2P:
		for n in steinerNodes:
			coordSteinerX1.append(n[2])
			coordSteinerY1.append(n[3])
			coordXDic[n[1]] = n[2]
			coordYDic[n[1]] = n[3]
			color1.append('green')
		axs=ax.scatter(coordSteinerX1, coordSteinerY1, s = 10, c = color1, label = 'Steiner Knoten', zorder = 3)
	else:
		for n in steinerNodes:
			coordXDic[n[1]] = n[2]
			coordYDic[n[1]] = n[3]
			if s[n[1]].X>0.5:
				coordSteinerX1.append(n[2])
				coordSteinerY1.append(n[3])
				color1.append('green')
			else:
				coordSteinerX2.append(n[2])
				coordSteinerY2.append(n[3])
				color2.append('green')
		axs1 = ax.scatter(coordSteinerX1, coordSteinerY1, s = 15, marker='*', c = color1, label = 'Steiner Knoten mit Splitter', zorder = 3)
		axs2 = ax.scatter(coordSteinerX2, coordSteinerY2, s = 10, marker='o', c = color2, label = 'Steiner Knoten', zorder = 3)

	
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
	axk=ax.scatter(coordCustomersX, coordCustomersY, marker='^', s = 10, c = color, label = 'Kunden (leicht versetzt)', zorder = 3)
	
	for e in solutionEdges:
		if not P2P:
			ax.text(0.5*(coordXDic[e[2]]+coordXDic[e[3]]),0.5*(coordYDic[e[2]]+coordYDic[e[3]]), numberDic[e[2],e[3]], color='grey', fontsize=7,ha='center', va='top',zorder=4)	
		if e[0]=='assEdge1':
			ax.arrow(coordXDic[e[2]], coordYDic[e[2]] , coordXDic[e[3]] - coordXDic[e[2]], coordYDic[e[3]] - coordYDic[e[2]], fc = "#00ff00" , ec = '#00ff00', head_width = 0, head_length = 0, width = 0.00001 , label='Anschlusskanten 1',zorder=1)
		elif e[0]=='assEdge2':
			ax.arrow(coordXDic[e[2]], coordYDic[e[2]] , coordXDic[e[3]] - coordXDic[e[2]], coordYDic[e[3]] - coordYDic[e[2]], fc = '#ff0066', ec = "#ff0066", head_width = 0, head_length = 0, width = 0.00001, label='Anschlusskanten 2',zorder=1)
		elif e[0]=='coreEdge':
			ax.arrow(coordXDic[e[2]], coordYDic[e[2]] , coordXDic[e[3]] - coordXDic[e[2]], coordYDic[e[3]] - coordYDic[e[2]], fc = "k", ec = "k", head_width = 0, head_length = 0, width = 0.00001, label='innere Kanten',zorder=2)

#fontsize : int or float or {'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'}
	ax.legend(fontsize='xx-small')
	dlinex1, = plt.plot([],[],color="#00ff00", linewidth=1)
	dlinex2, = plt.plot([],[],color='#ff0066', linewidth=1)
	dlinexc, = plt.plot([],[],color="k", linewidth=1)

	ax.legend([axl,axf1,axf2,axs1,axs2,axk,dlinexc,dlinex1,dlinex2],['Leitstellen','Facilitys mit Mulitplexer oder Splitter','Facilitys','Steinerknoten mit Splitter','Steinerknoten','Kunden (leicht versetzt)','innere Kanten','Anschlusskanten Glasfaser','Anschlusskanten Kupfer'],fontsize='xx-small')
	plt.show()
	#plt.savefig('test.png')                        


