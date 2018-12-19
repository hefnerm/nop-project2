# nop-project2
code for the second project of the lecture nop from Lucia Ortjohann and Moritz Hefner

packages you need:
	matplotlib
	gurobipy

to solve the problem ... run the file ...

	P2P with fiber 					script_fiberOnly.py
	P2P with fiber and copper		solveP2PFC.py
	P2MP with fiber 				script_solveP2MPF.py
	P2MP with fiber and copper		svript_solveP2MPF.py

in this files you can also change the parameters: 
	instance, demandFactor, period, splittingNumber and a lot more (highlighted with a lot of #)

other files:
	readWrite.py			reads the data
	preprocess.py			manly demand satisfaction and dijkstra
	graphalgs.py			some usefull tools for graphs
	datanice.py				splits the data into useful lists
	plotSolution.py			plots the solution
	solveOnlyFiber.py  		file to solve a part of the P2PF problem
	steinerflowmodel.py		gurobi model solves the steinertree problem with a flow formulation
	p2mpModelF.py 			gurobi model solves the P2MPF problem
	p2mpmodel.py 			gurobi model solves the P2MPFC problem

