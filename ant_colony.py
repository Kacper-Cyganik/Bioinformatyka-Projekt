import numpy as np

def goalFunction(solution, maxLen, spectGraph, oligo):
    oligolen = len(solution[0])
    maxcov = maxLen/oligolen * (oligolen-1)
    α = 0.7
    β = 1 - α
    A = 0
    B = oligolen
    for i in range(0, len(solution)-1):
        oligo1 = solution[i]
        oligo2 = solution[i+1]
        overlap = checkCov(oligo1, oligo2)
        A += oligolen - overlap 
        B += overlap
    A = ((maxcov - A)/maxcov)*α
    B = (abs(maxLen - B)/maxLen)*β
    result = B + A
    return result

def checkCov(oligo1, oligo2):
    matching = 0
    for j in range(0, len(oligo1)+1):
        finish = False
        for k in range(0, matching):
            end = oligo1[len(oligo1)-matching+k]
            start = oligo2[k]
            if (end != start):
                finish = True
                break
        if(finish):
            break
        matching += 1
    return len(oligo1) - matching + 1

def generateSolution(oligo, initNodeIndex, initNode, maxLen, spectOligos, weights, spectGraph, probabilities):
    solution = []
    solution.append(initNode)
    oligolen = len(initNode)
    currLen = oligolen
    currIndex = initNodeIndex
    
    while True:
        if sum(weights[currIndex]) == 0:
            return solution, goalFunction(solution, maxLen, spectGraph, oligo)
        choiceOligo = np.random.choice(oligo, p=weights[currIndex])
        choice = oligo.index(choiceOligo)
        overlap = checkCov(oligo[currIndex], oligo[choice])
        probabilities[currIndex][choice] /= 2
        for i in range(0, len(oligo)):
            weights[currIndex][i] = probabilities[currIndex][i]/sum(probabilities[currIndex])
        currLen += overlap
        solution.append(oligo[choice])
        currIndex = choice
        if currLen + overlap > maxLen:
            return solution, goalFunction(solution, maxLen, spectGraph, oligo)

def generateSolutions(colonySize, oligo, initNodeIndex, initNode, maxLen, spectOligos, probabilities, spectGraph):
    solutions = []
    weights = [[0 for column in range(len(oligo))] for row in range(len(oligo))]
    for i in range(0, len(oligo)):
        for j in range(0, len(oligo)):
            if sum(probabilities[i]) != 0:
                weights[i][j] = probabilities[i][j]/sum(probabilities[i])
    #print(weights)
    for i in range(0, colonySize):
        solutions.append(generateSolution(oligo, initNodeIndex, initNode, maxLen, spectOligos, weights, spectGraph, probabilities))
    return solutions

def compareSolutions(solutions):
    topTen = []
    solutions.sort(key=lambda row: (row[1]))
    for i in range(0, 10):
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
        print(probabilities)
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
