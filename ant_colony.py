import numpy as np
import utils
from config import N_DNA_CUT

class ACO:
    def goal_function(self, solution, max_len, spect_graph, oligo):

        oligolen = len(solution[0])
        maxcov = max_len/oligolen * (oligolen-1)

        a = 0.7
        b = 1 - a

        A = 0
        B = oligolen

        for i in range(0, len(solution)-1):
            oligo1 = solution[i]
            oligo2 = solution[i+1]
            overlap = N_DNA_CUT-utils.check_overlap(oligo1, oligo2)+1
            A += oligolen - overlap
            B += overlap
        A = ((maxcov - A)/maxcov)*a
        B = (abs(max_len - B)/max_len)*b
        result = B + A
        return result


    def generate_solution(self, oligo, initNodeIndex, initNode, maxLen, spectOligos, weights, spectGraph, probabilities):
        solution = []
        solution.append(initNode)
        oligolen = len(initNode)
        currLen = oligolen
        currIndex = initNodeIndex

        while True:
            if sum(weights[currIndex]) == 0:
                return solution, self.goal_function(solution, maxLen, spectGraph, oligo)
            choiceOligo = np.random.choice(oligo, p=weights[currIndex])
            choice = oligo.index(choiceOligo)
            overlap = N_DNA_CUT-utils.check_overlap(oligo[currIndex], oligo[choice])+1
            probabilities[currIndex][choice] /= 2
            for i in range(0, len(oligo)):
                weights[currIndex][i] = probabilities[currIndex][i] / \
                    sum(probabilities[currIndex])
            currLen += overlap
            solution.append(oligo[choice])
            currIndex = choice
            if currLen + overlap > maxLen:
                return solution, self.goal_function(solution, maxLen, spectGraph, oligo)

    def generate_solutions(self, colonySize, oligo, initNodeIndex, initNode, maxLen, spectOligos, probabilities, spectGraph):
        solutions = []
        weights = [[0 for _ in range(len(oligo))] for _ in range(len(oligo))]
        for i in range(0, len(oligo)):
            for j in range(0, len(oligo)):
                if sum(probabilities[i]) != 0:
                    weights[i][j] = probabilities[i][j]/sum(probabilities[i])
        for i in range(0, colonySize):
            solutions.append(self.generate_solution(oligo, initNodeIndex, initNode,
                             maxLen, spectOligos, weights, spectGraph, probabilities))
        return solutions

    def compare_solutions(self, solutions):
        topTen = []
        solutions.sort(key=lambda row: (row[1]))
        for i in range(0, 10):
            topTen.append(solutions[i])
        return topTen

    def pheromone_update(self, topTen, pheromones, oligo, evaporationRate):
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

    def run(self, spectGraph, oligo, initNodeIndex, initNode, maxLen, spectOligos):
        generations = 10
        colonySize = 50
        evaporationRate = 0.65  # ile procent feromonów wyparuje po co iteracje
        alpha = 1  # waga feromonów
        beta = 7  # waga pokrycia
        pheromones = [[0 for column in range(len(oligo))]
                      for row in range(len(oligo))]
        probabilities = [[0 for column in range(
            len(oligo))] for row in range(len(oligo))]
        for i in range(0, len(oligo)):
            for j in range(0, len(oligo)):
                probabilities[i][j] = spectGraph[i][j]
            print(probabilities)
        i = 0
        while (i < generations):
            solutions = self.generate_solutions(
                colonySize, oligo, initNodeIndex, initNode, maxLen, spectOligos, probabilities, spectGraph)
            # print(solutions)
            topTen = self.compare_solutions(solutions)
            #print('Nowe wyniki')
            print(topTen[0][-1])
            pheromones = self.pheromone_update(
                topTen, pheromones, oligo, evaporationRate)
            # print(pheromones)
            for j in range(0, len(oligo)):
                for k in range(0, len(oligo)):
                    if (pheromones[j][k] != 0):
                        probabilities[j][k] = pheromones[j][k]**alpha * \
                            spectGraph[j][k]**beta
                    else:
                        probabilities[j][k] = 0.1**alpha * \
                            spectGraph[j][k]**beta
            # print(probabilities)
            i += 1
        return topTen


if __name__ == "__main__":
    pass