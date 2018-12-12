from gurobipy import *

def solve_P2MP(nodes, steinerNodes, coreEdges, assEdges, terminals, root, costDic, splitterCosts, nFiberCablesCombine):
	
	
	model = Model("Steiner tree problem with flow formulation and splitternodes")
	
	#variables
	
	#x-variables: x_i_j = n if edge ij is used n times in the Steiner tree
	x = {}
	for e in coreEdges:
		x[e[2], e[3]] = model.addVar(lb = 0, ub = len(terminals), vtype = GRB.INTEGER, obj = costs[e[2], e[3]], name = "x_" + str(e[2]) + str(e[3]))
	
	for e in assEdges:
		x[e[2], e[3]] = model.addVar(vtype = GRB.BINARY, obj = costs[e[2], e[3]], name = "x_" + str(e[2]) + str(e[3]))
	
	#s-variable: s_i = 1 if steinerNode i uses splitter
	s = {}
	for node in steinerNodes:
		s[node[1]] = model.addVar(vtype = GRB.BINARY, obj = splitterCosts, name = "s_" + str(node[1]))
	
	#y-varibales: y_i_j_t = 1 if edge ij is in the flow from r to t
	y = {}
	for e in edges:
		for t in terminals:
			y[e[2], e[3], t[1]] = model.addVar(vtype = GRB.BINARY, obj = 0, name = "y_" + str(e[2]) + str(e[3]) + str(t[1]))
	    
	model.update()
	
	for t in terminals:
		model.addConstr(quicksum(y[e[2], e[3], t[1]] for e in graphalgs.incoming(root[1], edges)) - quicksum(y[e[2], e[3], t[1]] for e in graphalgs.outgoing(root[1], edges)) == -1)
		model.addConstr(quicksum(y[e[2], e[3], t[1]] for e in graphalgs.incoming(t[1], edges)) - quicksum(y[e[2], e[3], t[1]] for e in graphalgs.outgoing(t[1], edges)) == 1)
		for i in nodes:
			if not i[1] == root[1]:
				if not i[1] == t[1]:
					model.addConstr(quicksum(y[e[2], e[3], t[1]] for e in graphalgs.incoming(i[1], edges)) - quicksum(y[e[2], e[3], t[1]] for e in graphalgs.outgoing(i[1], edges)) == 0)
	
	#(2)
	for t in terminals:
		for e in edges:
			model.addConstr(y[e[2], e[3], t[1]] <= x[e[2], e[3]])
	
	#(3)
	for steiner in steinerNodes:
		for incidentEdge in graphalgs.incoming(steiner[1], edges) + graphalgs.outgoing(steiner[1], edges):
			model.addConstr((s[steiner[1]] * (nFiberCablesCombine - 1) + 1) * quicksum(y[e[2], e[3], t[1]] for e in graphalgs.incoming(steiner[1], edges) for t in terminals) <= x[incidentEdge[2], incidentEdge[3]])
	
	#just splitter or dslam
	
	#
	#solve
	model.optimize()
	
	return