import random as rand # For randomization


class Agent:
	# Create a new agent.
	def __init__(self, opinion = rand.randint(-1,1), committed = False):
		# self.opinion = rand.randint(-1,1)

		self.opinion = opinion
		self.committed=committed
		

		
    
	#Interactions return Boolean whether succesful or not
	def BAMinteract(self,partner,chanceOfBadInteraction):
		#committed minority just quit
		if partner.committed:
			return rand.random() < chanceOfBadInteraction

		opinionToEspouse=self.opinion
		opinionTwo = partner.opinion

		#opposite opinions
		if set([opinionToEspouse,opinionTwo]) == {-1,1} and rand.random() < chanceOfBadInteraction :
			return True
		

		if self.opinion == 0:
			opinionToEspouse = rand.choice([-1,1])

		if opinionToEspouse == -1:
			partner.opinion = max(-1, partner.opinion-1)

		elif opinionToEspouse == 1:
			partner.opinion = min(1,partner.opinion + 1)



		return False


		
	