import os # For creating directories
import random as rand # For randomization
import sys # For getting command line arguments
import networkx as nx # For generating graphs
import math # For the floor function
import numpy as np # For plot drawing
import matplotlib.pyplot as plt # For plot display
import agent # Class instantiating simulated agents

# Set and iterate over simulation parameters
def main():
	params = {
		# Strings
		'PATH': 'opinionData',

		# Integers
		'N_STEPS': 20, # Number of time steps
		'N_AGENTS': 150, # Number of agents
		'N_CONNECTIONS': 3,# Number of Connections in Regular Graph
	}

	return run(params)



		

# Run a simulation
def run(params):
	# Create agents
	agents = []
	for i in range(params['N_AGENTS']):
		agents.append(agent.Agent())

	graph = nx.random_regular_graph(params['N_CONNECTIONS'],params['N_AGENTS'])

	neighbors = []

	for i in range(params['N_AGENTS']):
		neighbors.append(list(nx.neighbors(graph, i)))

	# Time step
	for step in range(params['N_STEPS']):
		# Randomize interaction order
		order = list(range(len(agents)))
		rand.shuffle(order)
		
		# Social learning phase
		for i in order:

			j = rand.randint(0, len(neighbors[i]) - 1)
			partner = agents[neighbors[i][j]]
			agents[i].interact(partner)

		# Record data	
		data = [[] for i in range(params['N_STEPS'] + 1)] 
		data[step] = [a.opinion for a in agents]
		
	labels = {}
	for i in range(len(agents)):
		labels[i] = agents[i].opinion

	# print(data)
	return graph,labels
	



	# Make sure the directory path exists
	if not os.path.isdir(params['PATH']):
		os.makedirs(params['PATH'])
	
	# Save data to a new directory
	path = create_dir(params)
	with open(path + '/results.csv', 'w') as file:
		for i in range(step):
			file.write(','.join(map(str, data[i])) + '\n')


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



# Make sure this is an independent process
if __name__ == '__main__':
	g,labels=main()


	pos = nx.spring_layout(g, k=.1, seed=3113794652)
	nx.draw(g,node_color='black',pos=pos)
	nx.draw_networkx_labels(g,pos, labels, font_size=16, font_color="white")
	plt.show()
