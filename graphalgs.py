def outgoing(node, edges):
	outgoingEdges = []
	for e in edges:
		if (e[2] == node):
			outgoingEdges.append(e)

	return outgoingEdges


def incoming(node, edges):
	incomingEdges = []
	for e in edges:
		if (e[3] == node):
			incomingEdges.append(e)

	return incomingEdges