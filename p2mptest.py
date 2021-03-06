from gurobipy import *

import graphalgs


def solve_P2MPModel(nodes,edges,root,cos,facilitys,facilitys1,facilitys2,customers,steinerNodes,coreEdges,assEdges1,assEdges2,costs,M,splittingNumber,splitterCosts,timelimit):
	
	model=Model("P2MP")

	model.Params.timelimit=timelimit
	
	#variables
	
	#x-variables: x_i_j =1 if edge ij is in the Steiner tree
	x={}
	for e in edges:
		if e[0]=='assEdge1':
			x[e[2],e[3]]=model.addVar(vtype=GRB.INTEGER,lb=0,ub=len(customers),obj=costs[tuple(e)]+costs[e[2]],name="x_"+str(e[2])+'__'+str(e[3]))
		else:
			x[e[2],e[3]]=model.addVar(vtype=GRB.INTEGER,lb=0,ub=len(customers),obj=costs[tuple(e)],name="x_"+str(e[2])+'__'+str(e[3]))
	
	
	
	#y-varibales: y_i_j_t if edge ij is in the flow from r to t
	y={}
	for t in customers:
		for e in edges:
			y[e[2],e[3],t[1]]=model.addVar(vtype=GRB.BINARY,obj=0,name="y_"+str(e[2])+'__'+str(e[3])+'__'+str(t[1]))
	
	
	s={}
	for i in facilitys+steinerNodes+cos:
		if not i[1]==root[1]:
			s[i[1]]=model.addVar(vtype=GRB.BINARY,obj=splitterCosts,name="s_"+str(i[1]))
	
	m={}
	for i in facilitys2:
		m[i[1]]=model.addVar(vtype=GRB.BINARY,obj=costs[i[1]],name="m_"+str(i[1]))
	
	model.update()
	
	#print(graphalgs.incoming(root[1], edges))
	#print(graphalgs.outgoing(root[1], edges))
	#constraints
	for t in customers:
		#model.addConstr(quicksum(y[e[2],e[3],t[1]] for e in graphalgs.incoming(root[1],edges)) - quicksum(y[e[2],e[3],t[1]] for e in graphalgs.outgoing(root[1],edges)) == -1)
		#model.addConstr(quicksum(y[e[2],e[3],t[1]] for e in graphalgs.incoming(t[1],edges)) - quicksum(y[e[2],e[3],t[1]] for e in graphalgs.outgoing(t[1],edges)) == 1)
		
		model.addConstr(quicksum(y[e[2],e[3],t[1]] for e in graphalgs.outgoing(root[1],edges)) == 1)
		model.addConstr(quicksum(y[e[2],e[3],t[1]] for e in graphalgs.incoming(t[1],edges)) == 1)
		
		for i in nodes:
			if not (i[1]==root[1] or i[1]==t[1]):
				model.addConstr(quicksum(y[e[2],e[3],t[1]] for e in graphalgs.incoming(i[1],edges)) - quicksum(y[e[2],e[3],t[1]] for e in graphalgs.outgoing(i[1],edges)) == 0)
	
	for t in customers:
		for e in edges:
			model.addConstr(y[e[2], e[3], t[1]] <= x[e[2], e[3]])        
	
	for i in steinerNodes+facilitys1+cos:
		if not i[1]==root[1]:
			model.addConstr(quicksum(x[e[2],e[3]] for e in graphalgs.incoming(i[1],edges)) - quicksum(x[e[2],e[3]] for e in graphalgs.outgoing(i[1],edges)) <= 0)
			model.addConstr(quicksum(x[e[2],e[3]] for e in graphalgs.incoming(i[1],edges)) - quicksum(x[e[2],e[3]] for e in graphalgs.outgoing(i[1],edges)) >= -(splittingNumber-1)*s[i[1]])
	
	#for k in customers:
#		model.addConstr(quicksum(x[e[2],e[3]] for e in graphalgs.incoming(k[1],edges)) == 1)
	
	for i in facilitys2:
		model.addConstr(quicksum(x[e[2],e[3]] for e in graphalgs.incoming(i[1],edges)) - m[i[1]] - quicksum(x[e[2],e[3]] for e in graphalgs.outgoing(i[1],assEdges1+coreEdges)) <= 0)
		model.addConstr(quicksum(x[e[2],e[3]] for e in graphalgs.incoming(i[1],edges)) - m[i[1]] - quicksum(x[e[2],e[3]] for e in graphalgs.outgoing(i[1],assEdges1+coreEdges)) >= -(splittingNumber-1)*s[i[1]])
	
	for i in facilitys2:
		model.addConstr(s[i[1]]+m[i[1]] <= 1)
	
	for e in assEdges2:
		model.addConstr(x[e[2],e[3]]<=m[e[2]])
	
	for e in edges:
		if (e[0]=='assEdge1' or e[0]=='assEdge2'):
			if (costs[e[2],e[3]]<=0):
				model.addConstr(x[e[2],e[3]] <= quicksum(y[e[2],e[3],t[1]] for t in terminals))
	
	#solve
	model.optimize()
	
	#solution
	solution=[]
	if (model.status==2):
		for e in edges:
			if x[e[2],e[3]].x>0.5:
				solution.append(e)
	
	#testSol = open('./testSol.txt',"w")
	#for e in edges:
	#	testSol.write(str(e) + str(x[e[2], e[3]]) + "\n")
	
	#for t in customers:
	#	for e in edges:
	#		testSol.write(str(e) + str(y[e[2], e[3], t[1]]) + "\n")
	#testSol.close()
	
#	for t in customers:
#		setOne = False
#		for e in edges:
#			if e[3] == root[1]:
#				if y[e[2], e[3], t[1]].X == 1:
#					print("STH THAT SHOULDNT HAPPEN")
#					print(e[2], e[3], t[1],"\n")
#			elif e[2] == root[1]:
#				if y[e[2], e[3], t[1]].X == 1:
#					#print("edge set on 1: y_", e[2],"_", e[3], "_",t[1])
#					setOne = True
#		if not setOne:
#			print("for terminal ",t, " there is not outgoing edge from the root")
	
#	nWrongEdgeConstr = 0
#	for t in customers:
#		for e in edges:
#			if y[e[2], e[3], t[1]].X == 1 and x[e[2], e[3]].X == 0:
#				#print("WRONG!!!!!!!!!!!")
#				nWrongEdgeConstr = nWrongEdgeConstr + 1
	
	
#	nWrongAss2 = 0
	
#	for e in assEdges2:
#		if x[e[2],e[3]].X == 1 and m[e[2]].X == 0:
#			nWrongAss2 = nWrongAss2 + 1
#	
#	print("nAssEdges2: ", len(assEdges2))
#	print("nWrongAssEdges2: ", nWrongAss2)
#	
#	print("total edge constr: ", len(customers)*len(edges))
#	print("nWrongEdgeConstr: ", nWrongEdgeConstr)
	
	
	
	
	
	return model, x, y, s, m, solution