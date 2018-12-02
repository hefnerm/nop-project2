#dijkstra per hand
#knoten per hand usw

import steinerflussmodel


import readWrite

dataDic, costDic = readWrite.read('n')

nodes=dataDic['nodes']
edges=datatDic['edges']


#Knoten CO+Facilitys+Customers
nodes=[1,2,3,4,5,6,7,8,9,10,11,12]
#Customers
terminals=[9,10,11,12]
#CO
root=1
#Kanten: Co->Facilities+ alle assignment edges
edges=[[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[2,9],[2,10],[2,11],[2,12],[3,9],[4,10],[5,10],[6,11],[6,12],[7,11],[8,12]]

#Kosten: Co->Facitlites2: Wegkosten+Multiplexeraufbau, Co-> Facilities1: Wegkosten, Facilites2->Customers: Kupferkosten, Facilties1 -> Customers: Glasfaseranschlusskosten (1500)
costs={(1,2):4900,(1,3):18400,(1,4):20900,(1,5):24000,(1,6):10500,(1,7):17600,(1,8):22400,(2,9):110,(2,10):110,(2,11):110,(2,12):110,(3,9):1500,(4,10):110,(5,10):1500,(6,11):110,(6,12):110,(7,11):1500,(8,12):1500}

model,solution=steinerflowmodel.solve_steinerflowmodel(nodes,terminals,root,edges,costs)
print(solution) 