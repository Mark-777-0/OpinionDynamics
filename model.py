#Mark Ralston Daniel (260907915) built ontop of code provided by Marcel Montrey

import os # For creating directories
import random as rand # For randomization
import sys # For getting command line arguments
import networkx as nx # For generating graphs
import math # For the floor function
import numpy as np # For plot drawing
import matplotlib.pyplot as plt # For plot display
import agent # Class instantiating simulated agents
import copy 

# Set and iterate over simulation parameters
def main():
	params = {
		# Strings
		'PATH': 'opinionData',

		#Booleans
		'WRITING': True, #Recording data or not

		# Integers
		'N_RUNS': 1, # Number of time steps
		'N_STEPS': 100, # Number of time steps
		'N_AGENTS': 40, # Number of agents
		'N_CONNECTIONS': 4,# Number of Connections in Regular Graph
		

		#Floats
		'COMMITTED_RATIO': [0,1], # Ratio of Committed Agents Bs
		'OPINION_RATIO' : [.1,.2,.3,.4,.5,.6,.7,.8,.9], #Ratio that start B
		'P_BAD_INTERACTION': 0 #Probability of a bad interaction
	}
	# Parameters to iterate over
	itr = [p for p in params if isinstance(params[p], list)]

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
				elif len(itr) == 3:
					# Iterate over the second parameter
					for j in range(len(params[itr[2]])):
						# Set the second parameter
						runningParams[itr[2]] = params[itr[2]][j]
						
						# Set the runningParams path
						runningParams['PATH'] = '{0}/{1}={2}/{3}={4}/{5}={6}'.format(params['PATH'], itr[0], runningParams[itr[0]], itr[1], runningParams[itr[1]],itr[2],runningParams[itr[2]])
						
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
	# print([ agent.opinion for agent in agents])
	graph = nx.random_regular_graph(params['N_CONNECTIONS'],params['N_AGENTS'])

	#List of list of neighbors, [[],[],[]]
	neighbors = []

	for i in range(params['N_AGENTS']):
		neighbors.append(list(nx.neighbors(graph, i)))
	

	#Create list for storing opinion data
	data = [[] for i in range(params['N_STEPS'] + 1)] 


	
	# Time step
	for step in range(params['N_STEPS']):
		# Record data	
		# opinDict= {1:'A',-1:'B',0:0}
		data[step] = [a.opinion for a in agents]

		# Randomize interaction order
		order = list(range(len(agents)))
		rand.shuffle(order)
		
		
		# Opinion spreading phase
		for i in order:

			j = rand.randint(0, len(neighbors[i]) - 1)
			partner = agents[neighbors[i][j]]

			#Bad interaction
			if agents[i].BAMinteract(partner,params['P_BAD_INTERACTION']):
				adaptNetworkSimple(neighbors,i,j)
				
				
			
		
	
	labels = {}
	for i in range(len(agents)):
		labels[i] = agents[i].opinion
		
			
	
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

	
	return (graph,labels)


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
	length=len(neighbors[i]) - 1
	del neighbors[i][j]
	neighbors[i].append(rand.randint(0, length + 1))


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



# Make sure this is an independent process
if __name__ == '__main__':
	main( )
	# g,labels=main()

	# #Draw the graph
	# pos = nx.spring_layout(g, k=.1, seed=3113794652)
	# nx.draw(g,node_color='black',pos=pos)
	# nx.draw_networkx_labels(g,pos, labels, font_size=16, font_color="white")
	# plt.show()
