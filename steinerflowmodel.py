from gurobipy import *

import graphalgs

#solve Steiner tree problem with flow forumlation with gurobi
#nodes,terminals,roots as subset of nodes, edges as in dataDic, 
#costs ??
def solve_steinerflowmodel(nodes,terminals,root,edges,costs):
    
    model=Model("Steiner tree problem with flow formulation")
    
    #variables
    
    #x-variables: x_i_j =1 if edge ij is in the Steiner tree
    x={}
    for e in edges:
            x[e[2],e[3]]=model.addVar(vtype=GRB.BINARY,obj=costs[e[2],e[3]],name="x_"+str(e[2])+str(e[3]))

    #y-varibales: y_i_j_t if edge ij is in the flow from r to t
    y={}
    for e in edges:
        for t in terminals:
            y[e[2],e[3],t[1]]=model.addVar(vtype=GRB.BINARY,obj=0,name="y_"+str(e[2])+str(e[3])+str(t[1]))    
        
    model.update()
    
    #constraints
    #numerates as in the termpaper
    #(1)
    for t in terminals:
        model.addConstr(quicksum(y[e[2],e[3],t[1]] for e in graphalgs.incoming(root[1],edges)) - quicksum(y[e[2],e[3],t[1]] for e in graphalgs.outgoing(root[1],edges)) == -1)
        model.addConstr(quicksum(y[e[2],e[3],t[1]] for e in graphalgs.incoming(t[1],edges)) - quicksum(y[e[2],e[3],t] for e in graphalgs.outgoing(t[1],edges)) == 1)
        for i in nodes:
            if not i[1]==root[1]:
                if not i[1]==t[1]:
                     model.addConstr(quicksum(y[e[2],e[3],t[1]] for e in graphalgs.incoming(i[1],edges)) - quicksum(y[e[2],e[3],t[1]] for e in graphalgs.outgoing(i[1],edges)) == 0)

    #(2)
    for t in terminals:
        for e in edges:
            model.addConstr(y[e[2],e[3],t[1]] <= x[e[2],e[3]])

    #solve
    model.optimize()

    #solution
    solution=[]
    if (model.status==2):
        for e in edges:
            if x[e[2],e[3]].x>0.5:
                solution.append(e)

    return model,solution