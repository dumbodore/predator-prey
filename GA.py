from random import *
from predator import *
from subprocess import Popen
import sys

def generatePopulation():
	initialPopulation = []

	numGenes = 48
	populationSize = 50
	geneSize = 8

	for i in range(populationSize):
		tempChromosome = []

		for j in range(numGenes):
			tempGene = []
		
			for k in range(geneSize):

				k = randint(0, 1)
				tempGene.append(k)

			tempChromosome.append(tempGene)

		initialPopulation.append(tempChromosome)

	return initialPopulation


def toString(individual):

	builder = ""

	for gene in individual:
		for bit in gene:
			builder = builder + str(bit)

	return builder


def toList(chromosome):
	tempGene = []
	chromosomeList = []
	for bit in chromosome:
		if len(tempGene) == 8:
			chromosomeList.append(tempGene)
			tempGene = []
		tempGene.append(int(bit))
	chromosomeList.append(tempGene)
	return chromosomeList


# Returns fitness of individual in population 
def fitness(individual):

	strTeam = toString(individual)
	mid = len(strTeam) // 2
	strIndividualOne = strTeam[0:mid]
	strIndividualTwo = strTeam[mid:]

	# inputs chromosome to training bot file to get fitness
	cmd = ["python3", "predator.py", "-g", "SiriusBot", strIndividualOne]
	cmd2 = ["python3", "predator.py", "-g", "Dumbodore", strIndividualTwo]
	commands = [cmd, cmd2]

	procs = [ Popen(i) for i in commands ]
	for p in procs:
		p.wait()
	fit = open("fitness.txt", "r")
	fitnesses = fit.readlines()
	returnFit = 0
	fit.close()
	if len(fitnesses) == 2:
		fit1 = int(fitnesses[0])
		fit2 = int(fitnesses[1])
		
		if fit1 > fit2:
			returnFit = (fit1 * fit1)
		else:
			returnFit = (fit2 * fit2)
	elif len(fitnesses) == 1:
		fit1 = int(fitnesses[0])
		returnFit = (fit1 * fit1)
	else:
		returnFit = 1
	open("fitness.txt", "w").close()
	if returnFit == 0:
		returnFit = 1
	return returnFit

# Calculates fitness for each individual in population 
# and returns roulette wheel that will be used for selection
def rouletteWheel(population):

	populationFitness = []

	# calculate fitness for each individual in population 
	for i in range(len(population)):
		individualFitness = fitness(population[i])
		populationFitness.append(individualFitness)

	rouletteWheel = []

	# for each individual i in the population that has fitness value X, 
	# we add i X times to the rouletteWheel list. This is to essentially 
	# mimic an actual roulette wheel where the size of the slice for each 
	# individual corresponds to the fitness of the individual 
	for i in range(len(population)):
		temp = populationFitness[i]

		while temp > 0:
			rouletteWheel.append(i)
			temp = temp - 1 

	return rouletteWheel, populationFitness

# Returns two individuals that will be used for crossover
# rWheel: Roulette wheel used for selection 
def selection(rWheel, population):

	# randomly choose two people from population 
	indexOne = rWheel[randint(0, len(rWheel)-1)]
	
	# ensures that the same individual isn't picked twice
	indexTwo = -1 
	while (indexTwo == -1) or (indexTwo == indexOne):
		indexTwo = rWheel[randint(0, len(rWheel)-1)]

	individualOne = population[indexOne]
	individualTwo = population[indexTwo]
	
	# return two individuals
	return individualOne, individualTwo

# Return new individual that has been been crossed over from two parents.
def crossover(individualOne, individualTwo):

	parent1 = toString(individualOne)
	parent2 = toString(individualTwo)
	
	clength = len(parent1) # find length of each chromosome
	crossPoint = randint(0, clength - 1) # randomly generate the crossover point

	# store the values after the cross point of each parent
	cross1 = parent1[crossPoint:]
	cross2 = parent2[crossPoint:]

	# cross ending values
	child1 = parent1[:crossPoint]+cross2
	child2 = parent2[:crossPoint]+cross1

	rChild1 = toList(child1)
	rChild2 = toList(child2)

	return rChild1, rChild2


# Mutates bits in individual
def mutation(individual):
	
	# sets mutation value in large range

	# for each bit, generate a flip value 
	# and check whether it matches the mutation 
	# value. if it does, then flip that bit
	for i in range(len(individual)):

		for j in range(len(individual[i])):

			flip = randrange(0, 800)

			if flip == 1: #(1/800 chance)

				if individual[i][j] == 1:
					individual[i][j] = 0
				else: 
					individual[i][j] = 1

	return individual

# Main function
def evolve():

	population = generatePopulation()
	generations = 250
	newPopulation = []

	# used later 
	popFitness = []

	# number of generations to evolve 
	for i in range(generations):

		newPopulation = []

		# calculate fitness for all individuals in current population
		rWheel, popFitness = rouletteWheel(population)
		
		# create new population of individuals 
		while len(newPopulation) < 50:

			individualOne, individualTwo = selection(rWheel, population)
			tempIndividual1, tempIndividual2 = crossover(individualOne, individualTwo)
			newIndividual1 =  mutation(tempIndividual1)
			newIndividual2 =  mutation(tempIndividual2)
			newPopulation.append(newIndividual1)
			newPopulation.append(newIndividual2)

		
		bestFitness = max(popFitness)
		bestIndividual = population[popFitness.index(bestFitness)]
		overallFitness = sum(popFitness)/len(popFitness)
		print("Generation ", i, ":")
		print("Best individual: ", bestIndividual)
		print("Best individual's fitness: ", bestFitness)
		print("Overall population fitness: ", round(overallFitness, 4))
		print()

		with open('bestPeeps.txt', 'a') as inFile:
			outString = "Generation " + str(i) + ":" + "\t" + "Best individual's fitness: " + str(bestFitness) + "\t" + str(bestIndividual) + "\n"
			inFile.write(outString)


		population = newPopulation

	file = open("finalPopulation.txt", "w")
	index = 0
	for individual in population:

		## we write the individual and their fitness as one line in the file 
		fit = popFitness[index]
		person = str(individual)
		temp = person +  "\t" + str(fit) + "\n"
		file.write(temp)
		index = index + 1
	file.close()

	print("Final population written to file!")
evolve()

