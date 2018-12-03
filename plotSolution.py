import matplotlib.pyplot as plt

def plotSolution(facilitys,steinerNodes,cos,customers,solutionEdges,solutionRoot):

    
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
        coordXDic[n[1]]=n[2]
        coordYDic[n[1]]=n[3]
        flag=False
        for e in solutionEdges:
            if n[1]==e[2] or n[1]==e[3]:
                flag=True
        if flag:
            color.append('blue')
        else:
            color.append('#1aa3ff')
    ax.scatter(coordFacilitysX, coordFacilitysY, s=10, c=color, label='Facility nodes', zorder=2)

    coordCosX = []
    coordCosY = []

    color = []
    for n in cos:
        coordCosX.append(n[2])
        coordCosY.append(n[3])
        coordXDic[n[1]]=n[2]
        coordYDic[n[1]]=n[3]
        if n==solutionRoot:
            color.append('red')
        else:
            color.append('#E80000')
    ax.scatter(coordCosX, coordCosY, s=10, c=color, label='CO nodes', zorder=2)

    coordSteinerX = []
    coordSteinerY = []
    color = []
    for n in steinerNodes:
        coordSteinerX.append(n[2])
        coordSteinerY.append(n[3])
        coordXDic[n[1]]=n[2]
        coordYDic[n[1]]=n[3]
        color.append('green')
    ax.scatter(coordSteinerX, coordSteinerY, s=10, c=color, label='Steiner nodes', zorder=2)

    coordCustomersX = []
    coordCustomersY = []
    coordCustomerXDic = {}
    coordCustomerYDic = {}
    color = []
    for n in customers:
        coordCustomersX.append(n[2]+0.0002)
        coordCustomersY.append(n[3]+0.0002)
        coordXDic[n[1]]=n[2]+0.0002
        coordYDic[n[1]]=n[3]+0.0002
        color.append('orange')
    ax.scatter(coordCustomersX, coordCustomersY, s=10, c=color, label='Customer nodes (next to corresponding facility node)', zorder=2)

    for e in solutionEdges:
        ax.arrow(coordXDic[e[2]],coordYDic[e[2]] , coordXDic[e[3]]-coordXDic[e[2]], coordYDic[e[3]]-coordYDic[e[2]],fc="k", ec="k", head_width=0, head_length=0,width=0.00001)
    ax.legend()
    plt.show()

''' 

    t=[]
    for key, variable in transport.items():
        t.append(variable.x)
    maxTransport=max(t)
    
    for (p, c), variable in transport.items():
        if variable.x > 0:
            ax.arrow(coordPlants[p][0], coordPlants[p][1],
                     coordCustomers[c][0]-coordPlants[p][0],
                     coordCustomers[c][1]-coordPlants[p][1],
                     head_width=0.05, head_length=0.1, fc='k', ec='k',
                     length_includes_head=True, zorder=1,
                     width=0.015*variable.x/maxTransport)
            
    ax.legend()


    ##############vorlage:
    def plotSolution(coordCustomers, coordPlants, openPlant, transport):
    # visualize the location of plants and customers as circle and the 
    # transported goods as weighted arrows.

    plants = range(len(openPlant))
    customers = range(int(len(transport)/len(plants)))
    
    ax = plt.axes()
    ax.grid(True)
            
    # plot plants and customers as blue and orange circle in a coordinate
    # system
    coordPlantsX = []
    coordPlantsY = []
    label = []
    color = []
    for p in plants:
        coordPlantsX.append(coordPlants[p][0])
        coordPlantsY.append(coordPlants[p][1])
        label.append('P' + str(p))
        if openPlant[p].x > 0.5:
            color.append('blue')
        else:
            color.append('grey')
        ax.annotate("P"+str(p), (coordPlants[p][0]+0.05, coordPlants[p][1]+0.05), size=25)
    ax.scatter(coordPlantsX, coordPlantsY, s=100, c=color, label='Plants', zorder=2)
    
    coordCustomersX = []
    coordCustomersY = []
    for c in customers:
        coordCustomersX.append(coordCustomers[c][0])
        coordCustomersY.append(coordCustomers[c][1])
        coordAbove = (coordCustomers[c][0]+0.05, coordCustomers[c][1]+0.05)
        ax.annotate("C"+str(c), coordAbove, size=15)
    ax.scatter(coordCustomersX, coordCustomersY, s=100, c='orange', label='Customer', zorder=2)
    
    # compute max transport to indicate optimal transport by the width
    # of the arrows
    t=[]
    for key, variable in transport.items():
        t.append(variable.x)
    maxTransport=max(t)
    
    for (p, c), variable in transport.items():
        if variable.x > 0:
            ax.arrow(coordPlants[p][0], coordPlants[p][1],
                     coordCustomers[c][0]-coordPlants[p][0],
                     coordCustomers[c][1]-coordPlants[p][1],
                     head_width=0.05, head_length=0.1, fc='k', ec='k',
                     length_includes_head=True, zorder=1,
                     width=0.015*variable.x/maxTransport)
            
    ax.legend()
'''