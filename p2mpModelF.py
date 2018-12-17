from gurobipy import *

import graphalgs


def solve_P2MPModelFiber(nodes,edges,root,cos,facilitys,customers,steinerNodes,coreEdges,costs,splittingNumber,splitterCosts,timelimit):
	
	model=Model("P2MPG")

	model.Params.timelimit=timelimit
	
	#variables
	
	#x-variables: x_i_j =1 if edge ij is in the Steiner tree
	x={}
	for e in edges:
		if e[0]=='assEdge1':
			x[e[2],e[3]]=model.addVar(vtype=GRB.INTEGER,lb=0,ub=len(customers),obj=costs[tuple(e)]+costs[e[2]],name="x_"+str(e[2])+'__'+str(e[3]))
		else:
			x[e[2],e[3]]=model.addVar(vtype=GRB.INTEGER,lb=0,ub=len(customers),obj=costs[tuple(e)],name="x_"+str(e[2])+'__'+str(e[3]))
	
	
	
	#y-varibales: y_i_j_t=1 if edge ij is in the flow from r to t
	y={}
	for t in customers:
		for e in edges:
			y[e[2],e[3],t[1]]=model.addVar(vtype=GRB.BINARY,obj=0,name="y_"+str(e[2])+'__'+str(e[3])+'__'+str(t[1]))
	
	#s-varibales: s_i=1 if on node i is a splitter installed
	s={}
	for i in facilitys+steinerNodes:
		if not i[1]==root[1]:
			s[i[1]]=model.addVar(vtype=GRB.BINARY,obj=splitterCosts,name="s_"+str(i[1]))

	model.update()
	
	
	#constraints
	for t in customers:
		model.addConstr(quicksum(y[e[2],e[3],t[1]] for e in graphalgs.outgoing(root[1],edges)) == 1)
		model.addConstr(quicksum(y[e[2],e[3],t[1]] for e in graphalgs.incoming(t[1],edges)) == 1)
		
		for i in nodes:
			if not (i[1]==root[1] or i[1]==t[1]):
				model.addConstr(quicksum(y[e[2],e[3],t[1]] for e in graphalgs.incoming(i[1],edges)) - quicksum(y[e[2],e[3],t[1]] for e in graphalgs.outgoing(i[1],edges)) == 0)
	
	for t in customers:
		for e in edges:
			model.addConstr(y[e[2], e[3], t[1]] <= x[e[2], e[3]])        
	
	for i in steinerNodes+facilitys:
		if not i[1]==root[1]:
			model.addConstr(quicksum(x[e[2],e[3]] for e in graphalgs.incoming(i[1],edges)) - quicksum(x[e[2],e[3]] for e in graphalgs.outgoing(i[1],edges)) <= 0)
			model.addConstr(quicksum(x[e[2],e[3]] for e in graphalgs.incoming(i[1],edges)) - quicksum(x[e[2],e[3]] for e in graphalgs.outgoing(i[1],edges)) >= -(splittingNumber-1)*s[i[1]])


	for i in facilitys + steinerNodes:
		model.addConstr(s[i[1]] <= quicksum(x[e[2], e[3]] for e in graphalgs.incoming(i[1], edges)))
	#solve
	model.optimize()

	si={}
	for i in facilitys+steinerNodes+cos:
		if not i[1]==root[1]:
			si[i[1]]=s[i[1]].X
	
	#solution
	solution=[]
	if (model.status==2 or model.status==9):
		for e in edges:
			if x[e[2],e[3]].x>0.5:
				solution.append(e)

	
	return model, x, y, si, solution