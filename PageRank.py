from operator import itemgetter

# Declarations

edges=[]   #list of edges
nodes=[]
pagerank=[]
df=0.85 #damping factor



# Functions

def addEdge(edge):
	global edges
	edges+=[edge]


def extractEdges(inputfile):
	i=0
	edge=[]
	filePointer = open(inputfile, 'r')
	raw_list=filePointer.read().split()
	for var in raw_list:
		if i%3==0 and i!=0:
			addEdge(edge)
			edge=[]
		var1 = int(var)
		edge+=[var1]
		i+=1


def sortEdges():
	global edges
	edges.sort(key=itemgetter(0))		


def listNodes():
	global edges, nodes

	for i in edges:
		if i[0] not in nodes:
			nodes+=[i[0]]
		if i[1] not in nodes:
			nodes+=[i[1]]


def sortNodes():
	global nodes

	nodes.sort()


def sortPageRank():
	global pagerank

	pagerank.sort(key=itemgetter(1))		


def printPageRank():
	global pagerank

	f = open('result.txt', 'w')

	for i in pagerank:
		f.write("%s\n" % i)

	f.close()

def outgoingEdges(node):
	count=0

	for i in edges:
		if i[0]==node:
			count+=1

	return count


def calculatePageRank(node):
	global df, edges, nodes

	ratioSum=0
	pr=1-df
	pr=pr/len(nodes)

	for i in edges:
		if i[1]==node:
			n=outgoingEdges(i[0])
			wt=i[2]						#edge weight
			ratioSum=ratioSum+wt/n

	pr=pr+df*ratioSum

	return pr


# Data processing from txt

## File read

extractEdges('data/input.txt')

sortEdges()

listNodes()

sortNodes()

#Computing page rank for each node

for node in nodes:
	pr = calculatePageRank(node)
	pagerank+=[[node,pr]]

sortPageRank()

printPageRank()  #gives output in result.txt