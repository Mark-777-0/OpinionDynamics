import random as rand # For randomization


class Agent:
	# Create a new agent.
	def __init__(self):
		self.opinion = rand.randint(-1,1)
		
        
	def interact(self,partner):

		opinionToEspouse=self.opinion
		
		if self.opinion == 0:
			opinionToEspouse = rand.choice([-1,1])
	
		if opinionToEspouse == -1:
			partner.opinion = max(-1, partner.opinion-1)
		elif opinionToEspouse == 1:
			partner.opinion = min(1,partner.opinion + 1)



	