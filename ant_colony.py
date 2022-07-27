import numpy as np
import utils
from config import N_DNA_CUT


class ACO:

    def __init__(self, alpha=1, beta=7, colony_size=50, generations=10, evaporation_rate=0.65, spect_graph=None, oligo=None, init_node_index=0, init_node=None, max_len=500, spect_oligo=None):
        """initialize class with data

        Args:
            alpha (int, optional): ACO alpha. Defaults to 1.
            beta (int, optional): ACO beta. Defaults to 7.
            colony_size (int, optional): Colony size. Defaults to 50.
            generations (int, optional): Number of generations. Defaults to 10.
            evaporation_rate (float, optional): Evaporation rate. Defaults to 0.65.
            spect_graph (_type_, optional): 2d graph representing overlaping of nucleotides. Defaults to None.
            oligo (_type_, optional): list of nucleotides. Defaults to None.
            init_node_index (int, optional): index of starting node. Defaults to 0.
            init_node (_type_, optional): starting node. Defaults to None.
            max_len (int, optional): length of original DNA sequence. Defaults to 500.
            spect_oligo (_type_, optional): length of list of original DNA sequences . Defaults to None.
        """

        self.generations = generations
        self.colony_size = colony_size
        self.evaporation_rate = evaporation_rate
        self.alpha = alpha  # waga feromonów
        self.beta = beta  # waga pokrycia
        self.spect_graph = spect_graph
        self.oligo = oligo
        self.init_node_index = init_node_index
        self.init_node = init_node
        self.max_len = max_len
        self.spect_oligo = spect_oligo

        self.pheromones = [[0 for column in range(
            len(self.oligo))] for row in range(len(self.oligo))]
        self.probabilities = [[0 for column in range(
            len(self.oligo))] for row in range(len(self.oligo))]
        for i in range(0, len(self.oligo)):
            for j in range(0, len(self.oligo)):
                self.probabilities[i][j] = self.spect_graph[i][j]

    def _goal_function(self, solution):
        """ACO Goal function

        Args:
            solution (list): possible complementary dna sequence

        Returns:
            int : result
        """
        oligolen = len(solution[0])
        maxcov = self.max_len/oligolen * (oligolen-1)

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
        B = (abs(self.max_len - B)/self.max_len)*b
        result = B + A
        return result

    def _generate_solution(self, weights):
        solution = []
        solution.append(self.init_node)
        oligolen = len(self.init_node)
        currLen = oligolen
        currIndex = self.init_node_index

        while True:
            if sum(weights[currIndex]) == 0:
                return solution, self._goal_function(solution)
            choiceOligo = np.random.choice(self.oligo, p=weights[currIndex])
            choice = self.oligo.index(choiceOligo)
            overlap = N_DNA_CUT - \
                utils.check_overlap(
                    self.oligo[currIndex], self.oligo[choice])+1
            self.probabilities[currIndex][choice] /= 2
            for i in range(0, len(self.oligo)):
                weights[currIndex][i] = self.probabilities[currIndex][i] / \
                    sum(self.probabilities[currIndex])
            currLen += overlap
            solution.append(self.oligo[choice])
            currIndex = choice
            if currLen + overlap > self.max_len:
                return solution, self._goal_function(solution)

    def _generate_solutions(self):
        solutions = []
        weights = [[0 for x in range(len(self.oligo))]
                   for y in range(len(self.oligo))]
        for i in range(0, len(self.oligo)):
            for j in range(0, len(self.oligo)):
                if sum(self.probabilities[i]) != 0:
                    weights[i][j] = self.probabilities[i][j]/sum(self.probabilities[i])
        for i in range(0, self.colony_size):
            solutions.append(self._generate_solution(weights))
        return solutions

    def _compare_solutions(self, solutions):
        topTen = []
        solutions.sort(key=lambda row: (row[1]))
        for i in range(0, 10):
            topTen.append(solutions[i])
        return topTen

    def _pheromone_update(self, topTen):

        currIndex = 0
        nextIndex = 0
        for i in range(0, len(topTen)):
            for j in range(0, len(topTen[i][0])-1):
                currIndex = self.oligo.index(topTen[i][0][j])
                nextIndex = self.oligo.index(topTen[i][0][j+1])
                self.pheromones[currIndex][nextIndex] += topTen[i][1]
        for i in range(0, len(self.oligo)):
            for j in range(0, len(self.oligo)):
                self.pheromones[i][j] *= self.evaporation_rate
        return self.pheromones

    def run(self):

        i = 0
        while (i < self.generations):
            solutions = self._generate_solutions()
            # print(solutions)
            topTen = self._compare_solutions(solutions)
            #print('Nowe wyniki')
            print(topTen[0][-1])

            pheromones = self._pheromone_update(topTen)
            # print(pheromones)

            for j in range(0, len(self.oligo)):
                for k in range(0, len(self.oligo)):
                    if (pheromones[j][k] != 0):
                        self.probabilities[j][k] = pheromones[j][k]**self.alpha * \
                            self.spect_graph[j][k]**self.beta
                    else:
                        self.probabilities[j][k] = 0.1**self.alpha * \
                            self.spect_graph[j][k]**self.beta
            # print(probabilities)
            i += 1
        return topTen


if __name__ == "__main__":
    pass
