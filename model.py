#Mark Ralston Daniel (260907915) built from code provided by Marcel Montrey

from pyvis.network import Network #Network visualization
import os # For creating directories
import random as rand # For randomization
import sys # For getting command line arguments
import networkx as nx # For generating graphs
import math # For the floor function
import numpy as np # For plot drawing
import matplotlib.pyplot as plt # For plot display
import agent # Class instantiating simulated agents
import copy # Deep copying
import collections # Default dictionatires
import time # Speed testing

# Set and iterate over simulation parameters
def main():
	params = {
		# Strings
		'PATH': 'opinionData',

		#Booleans
		'WRITING': True, #Recording data or not

		# Integers
		'N_RUNS': 1, # Number of model simulations
		'N_STEPS': 1000, # Number of time steps
		'N_AGENTS': 1000, # Number of agents
		'N_CONNECTIONS': 15,# Number of Connections in Regular Graph
		
		#Floats
		'COMMITTED_RATIO': 1, # Ratio of Committed Agents Bs
		'OPINION_RATIO' : [.01,.05,.1,.25,.5,.75,.9], #Ratio that start B
		'P_BAD_INTERACTION': [0,.25,.5,.75,1] #Probability of a 
	}
	# Parameters to iterate over source venv/bin/activate
	itr = [p for p in params if isinstance(params[p], list)]
	# start = time.process_time()

	#iterate over the parameter with fewer settings first
	if len(itr) > 1 and len(params[itr[1]]) < len(params[itr[0]]):
		itr[0], itr[1] = itr[1], itr[0]
	for trial in range(params['N_RUNS']):
		for i in range(len(params[itr[0]])):
				# Set the first parameter
				runningParams = copy.deepcopy(params)
				runningParams[itr[0]] = params[itr[0]][i]
				
				# Print the runningParams parameter
				print('[{0}={1}]'.format(itr[0], runningParams[itr[0]]))
				
				# Iterating over only one parameter
				if len(itr) == 1:
					# Set the runningParams path
					runningParams['PATH'] = '{0}/{1}={2}'.format(params['PATH'], itr[0], runningParams[itr[0]])
					
					# Run 
					run(runningParams)
					
				# Iterating over two parameters
				elif len(itr) == 2:
					# Iterate over the second parameter
					for j in range(len(params[itr[1]])):
						# Set the second parameter
						runningParams[itr[1]] = params[itr[1]][j]
						
						# Set the runningParams path
						runningParams['PATH'] = '{0}/{1}={2}/{3}={4}'.format(params['PATH'], itr[0], runningParams[itr[0]], itr[1], runningParams[itr[1]])
						
						# Print the runningParams parameter
						print('  [{0}={1}]'.format(itr[1], runningParams[itr[1]]))
						
						# Run simulations in parallel
						run(runningParams)


# Run a simulation
def run(params):
	#add spacer to path
	# params['PATH']=params['PATH']+'/spacer'

	# Create agents
	agents = []
	for i in range(params['N_AGENTS']):
		
		if i < params['OPINION_RATIO'] * params['N_AGENTS']:
			if i < params['COMMITTED_RATIO']*params['OPINION_RATIO'] * params['N_AGENTS']:
				#committed = True, agent will not change opinions
				agents.append(agent.Agent(-1,True))
			else:
				agents.append(agent.Agent(-1))
		else:
			agents.append(agent.Agent(1))

	
	graph = nx.random_regular_graph(params['N_CONNECTIONS'],params['N_AGENTS'])

	#List of list of neighbors, [[],[],[]]
	neighborsAll=[]
	agentsAll=[]
	neighbors = []

	for i in range(params['N_AGENTS']):
		neighbors.append(list(nx.neighbors(graph, i)))
	
	#Create list for storing opinion data
	data = [[0 for j in range(2)] for i in range(params['N_STEPS'] + 1)] 
	data[0][0] = 'Committed_Agent'
	data[0][1] = 'Free_Agent' 

	dataNeighbor = [[0 for j in range(2)] for i in range(params['N_STEPS'] + 1)] 
	dataNeighbor[0][0] = 'B_Agent'
	dataNeighbor[0][1] = 'A_Agent' 


	# Time step
	for step in range(params['N_STEPS']):
		neighborsAll.append(copy.deepcopy(neighbors))
		agentsAll.append(copy.deepcopy(agents))
		# Record data	
		# opinDict= {1:'A',-1:'B',0:0}
		
		opinionCount=collections.Counter([a.opinion for a in agents])
		BtoBConnection=0
		AtoAConnection=0
		totalConnections=0
		for i,n in enumerate(neighbors):
			curOpn=agents[i].opinion
			curN=neighbors[i]
			for n in curN:
				totalConnections +=1
				if agents[n].opinion == curOpn and curOpn == -1:
					BtoBConnection += 1
				elif agents[n].opinion == curOpn and curOpn == 1:
					AtoAConnection +=1


		data[step + 1][0] =  opinionCount.get(-1,0)/ params['N_AGENTS']
		data[step + 1][1] = opinionCount.get(1,0) / params['N_AGENTS']

		dataNeighbor[step + 1][0] =  BtoBConnection/ opinionCount.get(-1,1)
		dataNeighbor[step + 1][1] = AtoAConnection / opinionCount.get(1,1)

		# Randomize interaction order
		order = list(range(len(agents)))
		rand.shuffle(order)
		
		
		# Opinion spreading phase
		for i in order:
			if len(neighbors[i]) >= 1:
				j = rand.randint(0, len(neighbors[i]) - 1)
			else:
				break
			
			partner = agents[neighbors[i][j]]

			#Bad interaction
			if agents[i].BAMinteract(partner,params['P_BAD_INTERACTION']):
				adaptNetworkSimple(neighbors,i,j)

				

	neighborOpinions = {}
	# for i in range(len(agents)):
	# 	total=0
	# 	for n in neighbors[i]:
	# 		total += agents[n].opinion

	# 	neighborOpinions[i] = total/len(neighbors)
		
			
	if (params['WRITING']):
	#Make sure the directory path exists
		if not os.path.isdir(params['PATH']):
			os.makedirs(params['PATH'])
		
		# Save data to a new directory
		path = create_dir(params)
		with open(path + '/results.csv', 'w') as file:
			# file.write(','.join(map(str, params.items())) + '\n')
			for i in range(step + 1):
				file.write(','.join(map(str, data[i])) + '\n')
	
	if (params['WRITING']):
	#Make sure the directory path exists
		params2=copy.deepcopy(params)
		params2['PATH'] = 'neighbor'+params2['PATH']
		if not os.path.isdir(params['PATH']):
			os.makedirs(params['PATH'])
	
		# Save data to a new directory
		
		path = create_dir(params2)
		with open(path + '/results.csv', 'w') as fileNeighbor:
			# file.write(','.join(map(str, params.items())) + '\n')
			for i in range(step + 1):
				fileNeighbor.write(','.join(map(str, dataNeighbor[i])) + '\n')

	return (graph, neighborsAll, agentsAll)


# Create a new numbered directory
def create_dir(params):
	dir = 0
	while os.path.isdir('{0}/{1}'.format(params['PATH'], dir)):
		dir += 1
	path = '{0}/{1}'.format(params['PATH'], dir)
	
	try:
		os.makedirs(path)
	except:
		path = create_dir(params)
	
	return(path)


def adaptNetworkSimple(neighbors,i,j):
	
	candidatesOne=list(range(len(neighbors)))
	candidatesTwo=list(range(len(neighbors)))

	neighborInd = neighbors[i][j]

	#trim down candidates
	candidatesOne.remove(i)

	#all neighbors, including the old one to be removed are removed
	for n in neighbors[i]:
		candidatesOne.remove(n)
	
	#do the same trimming down to the second list
	candidatesTwo.remove(neighborInd)
	for n2 in neighbors[neighborInd]:
		candidatesTwo.remove(n2)


	#remove, in case of undirected connection use if statement
	if neighbors[i][j] in neighbors[i]:
		neighbors[i].remove(neighbors[i][j])
	
	# if i in neighbors[neighborInd]:
	# 	neighbors[neighborInd].remove(i)

	#add random candidate
	if candidatesOne:
		newNeighborInd=rand.choice(candidatesOne)
		neighbors[i].append(newNeighborInd)
		# neighbors[newNeighborInd].append(i)

		# newNeighborInd2=rand.choice(candidatesTwo)
		# neighbors[neighborInd].append(newNeighborInd2)
		# neighbors[newNeighborInd2].append(neighborInd)



#def adaptNetworkRETIRED(neighbors,i,j):
	#length=len(neighbors[i]) - 1
	# # print(i,' --- ',j,'I AND J')
	# # print(neighbors)
	# neighborInd = neighbors[i][j]
	# # print("NEIGHBOR INDEX",neighborInd)
	# if neighbors[i][j] in neighbors[i]:
	# 	neighbors[i].remove(neighbors[i][j])
	# 	newNeighborInd=rand.randint(0, length + 1)
	# 	while newNeighborInd == neighborInd and newNeighborInd in neighbors[i] and newNeighborInd == i:
	# 		newNeighborInd=rand.randint(0, length + 1)	
	# 	neighbors[i].append(newNeighborInd)
	# 	neighbors[newNeighborInd].append(i)
	# if i in neighbors[neighborInd]:
	# 	neighbors[neighborInd].remove(i)
	# 	newNeighborInd2=rand.randint(0, length + 1)
	# 	while newNeighborInd2 == i and newNeighborInd2 in neighbors[neighborInd] and newNeighborInd2 != neighborInd:
	# 		neighbors[neighborInd].append(newNeighborInd2)
	# 		neighbors[newNeighborInd2].append(neighborInd)
	# # print("NEIGHBORS AFTER",neighbors)
	# # print('')

def adaptNetworkNeighbors(neighbors,i,j):
	
	length=len(neighbors[i]) - 1
	del neighbors[i][j]
	
	if (len(neighbors[i]) >= 1):
		counter = 0
		while (len(neighbors[i]) < length +1):
			randIndex= rand.choice(neighbors[i])
			randNeighbor = rand.choice(neighbors[randIndex])
			
			counter +=1 

			#not finding a friend just add a random
			if counter == 100:
				neighbors[i].append(rand.randint(0, length + 1))
			
			if i != randNeighbor and randNeighbor not in neighbors[i]:
				neighbors[i].append(randNeighbor)

	else:
		#find a new random neighbor if you had none
		neighbors[i].append(rand.randint(0, length + 1))

def plotGraph():
	graphParams = {
		# Strings
		'PATH': 'opinionData',

		#Booleans
		'WRITING': False, #Recording data or not

		# Integers
		'N_RUNS': 1, # Number of model simulations
		'N_STEPS': 20, # Number of time steps
		'N_AGENTS': 50, # Number of agents
		'N_CONNECTIONS': 10,# Number of Connections in Regular Graph
		

		#Floats
		'COMMITTED_RATIO': .2, # Ratio of Committed Agents Bs
		'OPINION_RATIO' : .5, #Ratio that start B
		'P_BAD_INTERACTION': .76, #Probability of a bad interaction
		}
	
	g, neighborsAll, agentsAll =run(graphParams)



	randLayout=nx.spring_layout(g,seed=123)
	

	for j,nList in enumerate(neighborsAll):
		newGraph=nx.Graph()
		curAgents=agentsAll[j]
		curNeighbors=neighborsAll[j]
		
		for i in range(graphParams['N_AGENTS']):
			if curAgents[i].opinion == -1:
				
				if curAgents[i].committed:
					newGraph.add_node(i,title='Committed Agent Negative Opinion ' + str(i),color='#3C3431',x=randLayout[i][0]*300,y=randLayout[i][1]*250)
					
					

				else:
					newGraph.add_node(i,title='Normal Agent Negative Opinion ' + str(i) ,color='#613659',x=randLayout[i][0]*300,y=randLayout[i][1]*250)
					
			elif curAgents[i].opinion == 1:
				newGraph.add_node(i,title='Normal Agent Positive Opinion ' + str(i),color='#76B947',x=randLayout[i][0]*300,y=randLayout[i][1]*250)
			else:
				newGraph.add_node(i,title='Normal Agent Neutral Opinion ' + str(i),color='#E1C391',x=randLayout[i][0]*300,y=randLayout[i][1]*250)
		
		
		for k,neighborList in enumerate(curNeighbors):
			for n in neighborList:
				newGraph.add_edge(k, n)


		nt = Network(height="750px", width="100%", filter_menu=True)
		nt.show_buttons(filter_=["physics"])
		nt.toggle_physics(False)
		
	# populates the nodes and edges data structures
		nt.from_nx(newGraph)
		nt.show( 'timeStep'+ str(j) +'nx.html' )
		
		print('Done ' + str(j + 1)+'/'+str(graphParams['N_STEPS']))


# You may either visualize trials, or run simulations
if __name__ == '__main__':
	##Run for statistic analysis of graphs
	# main()

	##Make a visual
	plotGraph()

	
		
		
	
