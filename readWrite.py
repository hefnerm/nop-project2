def read(instance):
	
	if instance == 'b':
		city = 'berlin-tu-maxDist600-blockR150-strat3.data'
	elif instance == 'n':
		city = 'naunyn-maxDist300-blockR50-strat3.data'
	elif instance == 'v':
		city = 'vehlefanz-maxDist1012-blockR300-strat3.data'
	else:
		raise Exception("incorrect input for data to read")
	
	data = open('./data/' + city ,"r")
	
	dat = {}
	
	for line in data:
		if line.find("#nCoreSteinerNodes") > -1:
			line = next(data)
			dat['nCoreSteinerNodes'] = int(line[0])
		
		if line.find("#nCoreFacilityNodes") > -1:
			line = next(data)
			dat['nCoreFacilityNodes'] = int(line[0])
		
		if line.find("#nCustomers") > -1:
			line = next(data)
			dat['nCustomers'] = int(line[0])
		
		if line.find("#nCO") > -1:
			line = next(data)
			dat['nCO'] = int(line[0])
		
		if line.find("#nFTypes") > -1:
			line = next(data)
			dat['nFTypes'] = int(line[0])
		
		if line.find("#nFPerType") > -1:
			line = next(data)
			tmp = line.split()
			dat['nFPerType'] = []
			for i in range(0, dat['nFTypes']):
				dat['nFPerType'].append(int(tmp[i]))
		
		if line.find("#nCoreEdges") > -1:
			line = next(data)
			dat['nCoreEdges'] = int(line[0])
		
		if line.find("#nAssEdgesPerType") > -1:
			line = next(data)
			tmp = line.split()
			dat['nAssEdgesPerType'] = []
			for i in range(0, dat['nFTypes']):
				dat['nAssEdgesPerType'].append(int(tmp[i]))
		
		if line.find("#SteinerNodes") > -1:
			line = next(data)
			dat['SteinerNodes'] = []
			while line[0][0] != '#':
				tmp = line.split()
				dat['SteinerNodes'].append([tmp[0], float(tmp[1]), float(tmp[2])])
				line = next(data)
		
		#check if numbers match
		
		if line.find("#FacilityNodes") > -1:
			line = next(data)
			dat['FacilityNodes'] = []
			while line[0][0] != '#':
				tmp = line.split()
				n = int(tmp[3])
				helpList = []
				for i in range(0,n):
					helpList = helpList + [int(tmp[3*i + 4]), int(tmp[3*i + 5]), int(tmp[3*i + 6])]
				dat['FacilityNodes'].append([tmp[0], float(tmp[1]), float(tmp[2]), n] + helpList)
				line = next(data)
		
		#check if numbers match
		
		if line.find("#CONodes") > -1:
			line = next(data)
			dat['CONodes'] = []
			while line[0][0] != '#':
				tmp = line.split()
				dat['CONodes'].append([tmp[0], float(tmp[1]), float(tmp[2]), float(tmp[3])])
				line = next(data)
		
		#check if numbers match
		
		if line.find("#CustomerNodes") > -1:
			line = next(data)
			dat['CustomerNodes'] = []
			while line[0][0] != '#':
				tmp = line.split()
				listHelp = []
				for i in range(0, dat['nFTypes']):
					listHelp.append(float(tmp[i + 4]))
				dat['CustomerNodes'].append([tmp[0], float(tmp[1]), float(tmp[2]), int(tmp[3])] + listHelp)
				line = next(data)
		
		#check if numbers match
		
		if line.find("#CoreEdges") > -1:
			line = next(data)
			dat['CoreEdges'] = []
			while line[0][0] != '#':
				tmp = line.split()
				dat['CoreEdges'].append([tmp[0], tmp[1], tmp[2], int(tmp[3]), float(tmp[4]), int(tmp[5])])
				line = next(data)
		
		#check if numbers match
		
		if line.find("#AssEdges1") > -1:
			line = next(data)
			dat['AssEdges1'] = []
			while line[0][0] != '#':
				tmp = line.split()
				dat['CoreEdges'].append([tmp[0], tmp[1], tmp[2], int(tmp[3]), int(tmp[4]), int(tmp[5])])
				line = next(data)
		
		#adjust to number iterator!!!!!!
		
		if line.find("#AssEdges2") > -1:
			line = next(data)
			dat['AssEdges2'] = []
			while line != None and line != '\n':
				tmp = line.split()
				dat['AssEdges2'].append([tmp[0], tmp[1], tmp[2], int(tmp[3]), int(tmp[4]), int(tmp[5])])
				line = next(data, None)
		
		#look above
		
		#adjust to FACILITYTYPESI
	
	
	
	data.close()
	
	return dat