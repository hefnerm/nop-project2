
def outgoing(node,edges):
	outgoingedges=[]
	for e in edges:
		if (e[2]==node):
			outgoingedges.append(e)

	return outgoingedges


def incomming(node,edges):
	incommingedges=[]
	for e in edges:
		if (e[3]==node):
			incommingedges.append(e)

	return incommingedges