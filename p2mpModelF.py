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
		s[i[1]]=model.addVar(vtype=GRB.BINARY,obj=splitterCosts,name="s_"+str(i[1]))
	
	model.update()
	
	
	#constraints
	#discribed and numerated as in the termpaper
	#(1)
	for t in customers:
		model.addConstr(quicksum(y[e[2],e[3],t[1]] for e in graphalgs.outgoing(root[1],edges)) == 1)
		model.addConstr(quicksum(y[e[2],e[3],t[1]] for e in graphalgs.incoming(t[1],edges)) == 1)
		
		for i in nodes:
			if not (i[1]==root[1] or i[1]==t[1]):
				model.addConstr(quicksum(y[e[2],e[3],t[1]] for e in graphalgs.incoming(i[1],edges)) - quicksum(y[e[2],e[3],t[1]] for e in graphalgs.outgoing(i[1],edges)) == 0)
	#(2)
	for t in customers:
		for e in edges:
			model.addConstr(y[e[2], e[3], t[1]] <= x[e[2], e[3]])        
	#(4)
	for i in steinerNodes+facilitys:
		if not i[1]==root[1]:
			model.addConstr(quicksum(x[e[2],e[3]] for e in graphalgs.incoming(i[1],edges)) - quicksum(x[e[2],e[3]] for e in graphalgs.outgoing(i[1],edges)) <= 0)
			model.addConstr(quicksum(x[e[2],e[3]] for e in graphalgs.incoming(i[1],edges)) - quicksum(x[e[2],e[3]] for e in graphalgs.outgoing(i[1],edges)) >= -(splittingNumber-1)*s[i[1]])
	
	#(3)
	for i in facilitys + steinerNodes:
		model.addConstr(s[i[1]] <= quicksum(x[e[2], e[3]] for e in graphalgs.incoming(i[1], edges)))
	#(5)
	for t in customers:
		for e in edges:
			if e[0] == 'assEdge1':
				if e[3] != t[1]:
					model.addConstr(y[e[2], e[3], t[1]] == 0)
	
	#solve
	model.optimize()
	
	
	
	#return solution
	solution = []	
	if model.status in [9, 11]:
		for e in edges:
			if x[e[2], e[3]].ub > 0.5:
				solution.append(e)
	
	if model.status == 2:
		for e in edges:
			if x[e[2], e[3]].X > 0.5:
				solution.append(e)
	
	si = {}
	for i in facilitys + steinerNodes:
		if model.status == 2:
			si[i[1]] = s[i[1]].X
		elif model.status in [9, 11]:
			si[i[1]] = s[i[1]].ub
	
	return model, x, y, si, solution