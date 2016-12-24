import numpy as np
import pandas as pd
import random as rn
import os
import operator


mutation_rate =  0.05
#population_size = 10
cross_over_rate = .35
#elitism_count = population_size*.2

data = pd.read_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\Files\\fitnessFinal.csv')
wck = pd.read_csv('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\Files\\wckt.csv')

players = set(data['Player'])
playerID = set([int(i) for i in data['PlayerID']])
wickeeperID = set([int(i) for i in wck['PlayerID']])

#print(data)
def playerIdMap():
	playerId = {}
	for i in range(len(players)):
		_id = int(data['PlayerID'][i])
		playerId[_id] = data['Player'][i]

	return playerId

playerIDMapping = playerIdMap()
def playerIDOverMap():
	playerIdOver = {}
	for i in range(len(players)):
		_id = int(data['PlayerID'][i])
		playerIdOver[_id] = float(data['Over'][i])

	return playerIdOver	

def playerIDBattingFit():
	playerIdBatfit = {}
	for i in range(len(players)):
		_id = int(data['PlayerID'][i])
		playerIdBatfit[_id] = float(data['BattingFitness'][i])

	return playerIdBatfit	

def playerIDBowlingFit():
	playerIdBowlfit = {}
	for i in range(len(players)):
		_id = int(data['PlayerID'][i])
		playerIdBowlfit[_id] = float(data['BowlingFitness'][i])

	return playerIdBowlfit

PlayerIdBowlfit = playerIDBowlingFit()
PlaperIdBatFit = playerIDBattingFit()

playerIdOver = playerIDOverMap()
w = list(wickeeperID)
def createIndividual():
	
	team = [rn.randint(1,len(players))]
	
	while len(team) != 13:
		p = rn.randint(1,len(players))
		if p in team:
			continue
		else:
			team.append(p)
	
	over = sum([ playerIdOver[i] for i in team ])

	while over < 30.0:
		index = rn.randint(0,12)
		team[index] = rn.randint(1,len(players))
		over = sum([ playerIdOver[i] for i in team ])

	r = rn.choice(w)
	while True:
		if r in team:
			r = rn.choice(w)
			continue
		else:
			team.append(r)
			break

	return team

def isIndividual(team):
	
	playerIdOver = playerIDOverMap()
	over = sum([ playerIdOver[i] for i in team ])
	return len(set(team))==14 and over >= 30	


def createPopulation(population_size=100):
	newPopulation = []
	for _ in range(population_size):
		newPopulation.append(createIndividual())

	return newPopulation


def getFitness(individual):
	
	battingFitness = 0
	bowlingFitness = 0
	
	for i in individual:
		battingFitness += PlaperIdBatFit[i]
		bowlingFitness += PlayerIdBowlfit[i]

	return (battingFitness - bowlingFitness)

def getFittestIndividual(pop):
	from operator import itemgetter
	newPopulation = []
	for i in pop:
		value = [i,getFitness(i)]
		newPopulation.append(value)

	return sorted(newPopulation, key=itemgetter(1),reverse = True)


def individualSelection(pop):

	Score = sum([pop[i][1] for i in range(len(pop))])
	wheelPosition = rn.random() * Score
	spinWheel = 0
	for i in range(len(pop)):
		spinWheel += pop[i][1]
		if spinWheel >= wheelPosition:
			return pop[i][0]

	return pop[len(pop)-1][0]

def crossOverPopulation(pop):

	elitism_count = len(pop)*.2
	newPopulation = []
	sortedpop = getFittestIndividual(pop)
	for i in range(len(pop)):
		parent1 = sortedpop[i][0]
		#print(parent1,'a')
		if cross_over_rate > rn.random() and i > elitism_count:

			parent2 = individualSelection(sortedpop)
			#print(parent2,'b')
			offspring = parent1[:7] + parent2[7:]

			if isIndividual(offspring):
				newPopulation.append(offspring)

		newPopulation.append(parent1)

	for i in range(len(pop)-len(newPopulation)):
		individual = createIndividual()
		newPopulation.append(individual)

	return newPopulation

'''
p = createPopulation(100)
newp = crossOverPopulation(p)
print(getFittestIndividual(p))
print('-------------------------')
print(getFittestIndividual(newp))
'''

def mutateIndividual(individual):

	index1 = rn.randint(0,7)
	index2 = rn.randint(8,13)

	if index2 == 13:
		individual[index2] = rn.choice(w)

	else:
		individual[index2] = rn.randint(1,len(playerID))

	individual[index1] = rn.randint(1,len(playerID))

	while not isIndividual(individual):
		index = rn.randint(0,12)
		individual[index] = rn.randint(1,len(playerID))	

	return individual


def mutatePopulation(pop): #pop = [[individual],fitness]
	newPopulation = []
	elitism_count = len(pop)*.2
	sortedpop = getFittestIndividual(pop)
	for i in range(len(pop)):
		team = sortedpop[i][0]
		if mutation_rate > rn.random() and elitism_count < i:
			individual = mutateIndividual(sortedpop[i][0])
			newPopulation.append(individual)
		newPopulation.append(team)

	return newPopulation

'''
p = createPopulation(100)
newp = mutatePopulation(p)
print(getFittestIndividual(p))
print('-------------------------')
print(getFittestIndividual(newp))
'''

def evolve(pop):
	teamFitness = []  #team fitness 
	from operator import itemgetter
	for i in pop:
		teamFit = [i, getFitness(i)]
		teamFitness.append(teamFit)
	
	return sorted(teamFitness, key=itemgetter(1),reverse = True)
	

def GeneticAlgorithm():

	GenerationFitness = []

	generation = 0
	population = createPopulation(100)
	populationFitness = evolve(population)
	generation = 1

	while generation < 50:

		value = [populationFitness[0][0],generation,populationFitness[0][1]]#[team,gen,fitness]
		f.write(str(value)+os.linesep)
		print(value)
		population = crossOverPopulation(population)

		population = mutatePopulation(population)

		populationFitness = getFittestIndividual(population)

		generation += 1

		GenerationFitness.append(value)

		#print(generation)

	return GenerationFitness

try:
	f = open('C:\\Users\\tesla\\Dropbox\\Thesis-Work\\Code\\out.txt','w')
except:
	print('File not found!')
result = GeneticAlgorithm()
f.write(str(result[-1]))


#[26, 28, 1, 37, 15, 13, 35, 42, 34, 20, 60, 31, 50, 25] ----  50 generation
#[34, 45, 65, 28, 18, 48, 1, 35, 54, 47, 22, 23, 8, 38], 19, 108.85999999999996]