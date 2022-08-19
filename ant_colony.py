from audioop import avg
import time
from unittest import result
import numpy as np
import utils
from config import N_DNA_CUT

class ACO:

    def __init__(self, alpha=1, beta=7, colony_size=50, generations=10, runtime = 10, evaporation_rate=0.65, spect_graph=None, oligo=None, init_node_index=0, init_node=None, max_len=500, spect_oligo=None):
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
        self.runtime = 60000 * runtime
        self.colony_size = colony_size
        self.evaporation_rate = 1 - evaporation_rate
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
        for i in range(0, len(self.oligo)):
            for j in range(0, len(self.oligo)):
                self.pheromones[i][j] = self.spect_graph[i][j]

        self.topTen = []

    def _goal_function(self, solution):
        """ACO Goal function

        Args:
            solution (list): possible complementary dna sequence

        Returns:
            int : result
        """

        a = 0.4
        b = 1 - a

        oligolen = len(solution[0])
        maxcov = self.max_len/oligolen * (oligolen-1)
        maxnodes = self.max_len - oligolen + 1
        A = 0
        B = len(solution)
        for i in range(0, len(solution)-1):
            oligo1 = solution[i]
            oligo2 = solution[i+1]
            overlap = N_DNA_CUT-utils.check_overlap(oligo1, oligo2)+1
            A += oligolen - overlap
        return a-((maxcov - A)/maxcov)*a + ((maxnodes - B)/maxnodes)*b

    def _generate_solution(self, weights):
        solution = []
        solution.append(self.init_node)
        oligolen = len(self.init_node)
        currLen = oligolen
        currIndex = self.init_node_index

        while True:
            if sum(weights[currIndex]) == 0: #no road to progress
                if len(utils.squash(solution)) != self.max_len:
                    return [solution, abs(len(utils.squash(solution)) - self.max_len)] #throw away this solution
                else:
                    return [solution, self._goal_function(solution)] #I guess it was just the end
            if len(utils.squash(solution)) == self.max_len: #the length checks out
                return [solution, self._goal_function(solution)] #It's a passible solution
           

            choiceOligo = np.random.choice(self.oligo, p=weights[currIndex])
            choice = self.oligo.index(choiceOligo)
            overlap = utils.check_overlap(self.oligo[currIndex], self.oligo[choice])+1
            self.pheromones[currIndex][choice] /= 2
            for i in range(0, len(self.oligo)):
                weights[currIndex][i] = self.pheromones[currIndex][i] / sum(self.pheromones[currIndex])
            currLen += overlap
            solution.append(self.oligo[choice])
            currIndex = choice


    def _generate_solutions(self):
        solutions = []
        weights = [[0 for x in range(len(self.oligo))]
                   for y in range(len(self.oligo))]
        for i in range(0, len(self.oligo)):
            for j in range(0, len(self.oligo)):
                if sum(self.pheromones[i]) != 0:
                    weights[i][j] = self.pheromones[i][j]/sum(self.pheromones[i])
        for i in range(0, self.colony_size):
            solutions.append(self._generate_solution(weights))
        return solutions

    def _compare_solutions(self, solutions):
        solutions.sort(key=lambda row: (row[1]))
        self.topTen = self.topTen[:3]
        for i in range(0, 10):
            self.topTen.append(solutions[i])
        self.topTen.sort(key=lambda row: (row[1]))
        self.topTen = self.topTen[:10]

    def _pheromone_update(self, topTen):
        mean = np.mean(self.pheromones)
        tolerance = 0.2*mean
        for i in range(0, len(self.oligo)):
            for j in range(0, len(self.oligo)):
                self.pheromones[i][j] *= self.evaporation_rate
                if self.pheromones[i][j] > 100:
                    self.pheromones[i][j] = 100
                if self.pheromones[i][j] > mean + tolerance:
                    self.pheromones[i][j] -= tolerance
                if self.pheromones[i][j] < mean - tolerance and self.pheromones[i][j] > tolerance:
                    self.pheromones[i][j] += tolerance
                
        currIndex = 0
        nextIndex = 0
        for result in topTen:
            result = result[0]
            for i in range(len(result)-1):
                currIndex = self.oligo.index(result[i])
                nextIndex = self.oligo.index(result[i+1])
                self.pheromones[currIndex][nextIndex] += self.max_len/utils.check_overlap(result[i], result[i+1])

        #print(self.pheromones)

    def run(self):
        i = 0
        while (i < self.generations):
            print('generacja: ', i)
            solutions = self._generate_solutions()
            self._compare_solutions(solutions)
            print("goal: ", self.topTen[0][-1])

            self._pheromone_update(self.topTen)

            i += 1
        print(self.pheromones)
        return self.topTen


if __name__ == "__main__":
    pass
