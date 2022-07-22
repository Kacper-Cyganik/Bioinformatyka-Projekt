import numpy as np

def generateSolution(oligo, initNodeIndex, initNode, maxLen, spectOligos, weights, spectGraph, probabilities):
    solution = []
    solution.append(initNode)
    currLen = len(initNode)
    currIndex = initNodeIndex
    length = 1
    
    while(currLen < maxLen):
        choiceOligo = np.random.choice(oligo, p=weights[currIndex])
        choice = oligo.index(choiceOligo)
        choiceCost = spectGraph[currIndex][choice]
        probabilities[currIndex][choice] /= 2
        for i in range(0, len(oligo)):
            weights[currIndex][i] = probabilities[currIndex][i]/sum(probabilities[currIndex])

        #print(choiceOligo, choice, choiceCost, weights[currIndex][choice])
        #print(weights[currIndex])

        currLen += (len(initNode) - choiceCost)
        if (currLen > maxLen):
            currLen -= (len(initNode) - choiceCost)
            currIndex = choice
            return solution, length/spectOligos
        solution.append(oligo[choice])
        currIndex = choice
        length += 1
    #print(solution)
    return solution, length/spectOligos

def generateSolutions(colonySize, oligo, initNodeIndex, initNode, maxLen, spectOligos, probabilities, spectGraph):
    solutions = []
    weights = [[0 for column in range(len(oligo))] for row in range(len(oligo))]
    for i in range(0, len(oligo)):
        for j in range(0, len(oligo)):
            weights[i][j] = probabilities[i][j]/sum(probabilities[i])
    #print(weights)
    for i in range(0, colonySize):
        solutions.append(generateSolution(oligo, initNodeIndex, initNode, maxLen, spectOligos, weights, spectGraph, probabilities))
    return solutions

def compareSolutions(solutions):
    topTen = []
    solutions.sort(key=lambda row: (row[1]), reverse=True)
    for i in range(0, 19):
        topTen.append(solutions[i])
    return topTen

def pheromoneUpdate(topTen, pheromones, oligo, evaporationRate):
    currIndex = 0
    nextIndex = 0
    for i in range(0, len(topTen)):
        for j in range(0, len(topTen[i][0])-1):
            currIndex = oligo.index(topTen[i][0][j])
            nextIndex = oligo.index(topTen[i][0][j+1])
            pheromones[currIndex][nextIndex] += topTen[i][1]
    for i in range(0, len(oligo)):
        for j in range(0, len(oligo)):
            pheromones[i][j] *= evaporationRate       
    return pheromones

def antColony(spectGraph, oligo, initNodeIndex, initNode, maxLen, spectOligos):
    generations = 10
    colonySize = 50
    evaporationRate = 0.65 #ile procent feromonów wyparuje po co iteracje
    alpha = 1 #waga feromonów
    beta = 7 #waga pokrycia
    pheromones = [[0 for column in range(len(oligo))] for row in range(len(oligo))]
    probabilities = [[0 for column in range(len(oligo))] for row in range(len(oligo))]
    for i in range(0, len(oligo)):
        for j in range(0, len(oligo)):
            probabilities[i][j] = spectGraph[i][j]
    i = 0
    while (i < generations):
        solutions = generateSolutions(colonySize, oligo, initNodeIndex, initNode, maxLen, spectOligos, probabilities, spectGraph)
        #print(solutions)
        topTen = compareSolutions(solutions)
        #print('Nowe wyniki')
        print(topTen[0][-1])
        pheromones = pheromoneUpdate(topTen, pheromones, oligo, evaporationRate)
        #print(pheromones)
        for j in range(0, len(oligo)):
            for k in range(0, len(oligo)):
                if (pheromones[j][k] != 0):
                    probabilities[j][k] = pheromones[j][k]**alpha * spectGraph[j][k]**beta
                else:
                    probabilities[j][k] = 0.1**alpha * spectGraph[j][k]**beta
        #print(probabilities)
        i += 1
    return topTen
