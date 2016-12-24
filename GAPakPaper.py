import pandas as pd
import numpy as np
import random as rn

df = pd.read_csv('fitness_pak_paper.csv')
dfLen = len(df)

#print(df)
idFitness = {}
for i in range(dfLen):
	idFitness[df['PlayerID'][i]] = df['fitness'][i]

Score = sum([ value for value in idFitness.values() ])

# Constant of GA for mutation , crossover, elitism
mutation_rate = .05
crossover_rate = .02


def listSelector(type):
	return [ df['PlayerID'][i] for i in range(dfLen) if df['Specification'][i]==type ]


# Return an individual team based on length = # of team member
def getIndividual():

	individual = []
	# Players 1-8 are considered for batsman
	batsmans = listSelector('BAT')
	individual.append(batsmans[rn.randint(0,len(batsmans)-1)])
	count = 1
	while count != 8:
		index = rn.randint(0,len(batsmans)-1)
		if batsmans[index] not in individual:
			individual.append(batsmans[index])
			count+=1

	# Player 9 is considered for wc
	wcks = listSelector('WC')
	individual.append(wcks[rn.randint(0,len(wcks)-1)])

	# Players 10-14 are considered for bowlers
	bowlers = listSelector('BOW')
	individual.append(bowlers[rn.randint(0,len(bowlers)-1)])
	count = 1
	while count != 5:
		index = rn.randint(0,len(bowlers)-1)
		if bowlers[index] not in individual:
			individual.append(bowlers[index])
			count+=1

	# Players 15-16 are considered for allRounder
	allRounders = listSelector('ALL')
	individual.append(allRounders[rn.randint(0,len(allRounders)-1)])
	count = 1
	while count != 2:
		index = rn.randint(0,len(allRounders)-1)
		if allRounders[index] not in individual:
			individual.append(allRounders[index])
			count+=1

	return individual

# Test individual method
# print(getIndividual())		

# Return number of population = length
def getPopulation(length):

	return [getIndividual() for _ in range(length)]

def calculateFitness(team):
	sum = 0
	for i in team:
		sum += idFitness[i]
	return sum

def avrgPopulationFitness(pop): # pop = population

	return sum([ calculateFitness(team) for team in pop ])/len(pop)

def crossOverPopulation(pop):
	newPopulation = [] 
	elitismCount = crossover_rate*len(pop)
	popFitness = [ (calculateFitness(individual),individual) for individual in pop ]

	for individual in sorted(popFitness):
		parent1 = individual[0]
		count = 0
		if crossover_rate > rn.random() and elitismCount > count:
			parent2 = rouletteWheelSelect(pop)
			offSpring = crossOver(parent1, parent2)
			newPopulation.append(offSpring)
		else:
			newPopulation.append(parent1)

	return newPopulation



def crossOver(parent1, parent2):
	return parent1[:8].extend(parent2[8:])

def rouletteWheelSelect(pop): # Score = sum of fitness list
	
	wheelPosition = rn.random * Score
	spinWheel = 0
	for individual in pop:
		spinWheel += calculateFitness(individual)
		if spinWheel >= wheelPosition:
			return individual

	return pop[len(pop)-1]

def mutation(individual):

	# Two point mutation 

	for _ in range(2):

		batsmans = listSelector('BAT')
		bowlers = listSelector('BOW')
		wicketkeepers = listSelector('WC')
		allRounders = listSelector('ALL')

		index = rn.randint(0,15)

		if index <= 8:
			player = batsmans[rn.randint(0,len(batsmans)-1)]
		elif index > 9 and index <= 14:
			player = bowlers[rn.randint(0,len(bowlers)-1)]
		elif index in [15,16]:
			player = allRounders[rn.randint(0,len(allRounders)-1)]
		elif index == 9:
			player = wicketkeepers[rn.randint(0,len(wicketkeepers)-1)]

		individual[index] = player
	
	return individual


