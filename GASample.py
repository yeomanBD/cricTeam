# Import section 

import random as rn
import operator as op

# Each Component of population
def individuals(length, _min, _max):
    ''' Return value between _min and _max value inclusive'''
    return [ rn.randint(_min, _max) for x in range(length) ]

def population(count, length, _min, _max):
	'''
	Return population 
	@param count # of individuals
	'''
	return [ individuals(length, _min, _max) for _ in range(count) ] 

def fitness(individual, target):
	''' @param target target-value '''
	return abs(target - sum(individual))

def avrg_population(population, target):
	avrg = [ fitness(individual, target) for individual in population ]

	return (avrg // len(population))

def evolve(population, target, survive_rate = .2,random_sel_rate = .05,mutation_rate = 0.01):

 	graded = [ (fitness(x, target), x) for x in population]
 	graded = [ x[1] for x in sorted(graded) ]
 	retain_length = int(len(graded)*survive_rate)
 	parents = graded[:retain_length]

 	'''Randomly select 5% of other population'''
 	for i in graded[retain_length:]:
 		if random_sel_rate > rn.random():
 			parents.append(i)


 	''' mutate some individuals'''
 	for individual in parents:
 		if mutation_rate > rn.random():
 			pos_to_mutate = rn.randint(0, len(individual)-1)

 			individual[pos_to_mutate] = rn.randint(min(individual),max(individual))


 	''' Crossover parents to create children'''
 	parents_length = len(parents)
 	desired_length = len(population) - parents_length
 	children = []

 	while len(children) < desired_length:
 		male = rn.randint(0, parents_length-1)
 		female = rn.randint(0, parents_length-1)
 		if male != female:
 			father = parents[male]
 			mother = parents[female]
 			half = len(father)//2
 			child = father[:half] + mother[half:]
 			children.append(child)

 	parents.extend(children)
 	return parents


target = 371
p_count = 100
i_length = 5
i_min = 0; i_max = 100;
p = population(p_count, i_length, i_min, i_max)
fitness_history = [avrg_population(p, target),]
for i in range(100):
	p = evolve(p, target)
	fitness_history.append(avrg_population(p,target))


    