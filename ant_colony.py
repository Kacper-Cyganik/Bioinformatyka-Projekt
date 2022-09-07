import numpy as np
import utils
from config import N_DNA_CUT, DEBUG


class ACO:

    def __init__(self, alpha=1, beta=7, colony_size=50, generations=10, evaporation_rate=0.65, spect_graph=None, oligo=None, init_node_index=0, init_node=None, max_len=500, spect_oligo=None, repetitions=None):
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
        self.evaporation_rate = 1 - evaporation_rate
        self.alpha = alpha  # waga feromonów
        self.beta = beta  # waga pokrycia
        self.spect_graph = spect_graph
        self.oligo = oligo
        self.init_node_index = init_node_index
        self.init_node = init_node
        self.max_len = max_len
        self.spect_oligo = spect_oligo
        self.repetitions = repetitions
        self.goal = 0

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

        a = 1.0
        b = 0.0
        c = 1 - a - b
        _, solution_repetitions = utils.generate_repetitions(solution)
        repetitions_check = utils.check_repetitions(
            self.repetitions, solution_repetitions)

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
        
        result = a-((maxcov - A)/maxcov)*a + ((maxnodes - B)/maxnodes)*b + c - c*repetitions_check

        if DEBUG:
            _, solution_repetitions = utils.generate_repetitions(solution)
            repetition_check = utils.check_repetitions(
                self.repetitions, solution_repetitions)
            print('possible solution goal function:', result,
                  'solution_repetitions', repetition_check)

        return result

    def _generate_solution(self, weights):
        solution = []
        solution.append(self.init_node)
        oligolen = len(self.init_node)
        currLen = oligolen
        currIndex = self.init_node_index
        self.goal = 0

        while True:
            choiceWeights = weights.copy()[currIndex]
            for i in range(len(choiceWeights)):
                # Zero weights if it makes the goal go down
                possibleNext = solution.copy()
                possibleNext.append(self.oligo[i])
                if (self._goal_function(possibleNext) < self.goal):
                    choiceWeights[i] = 0
            sumWeights = sum(choiceWeights)
            if sumWeights != 0:
                choiceWeights /= sumWeights
            if sum(weights[currIndex]) == 0:  # no road to progress
                if len(utils.squash(solution)) != self.max_len:
                    # throw away this solution
                    return [solution, abs(len(utils.squash(solution)) - self.max_len)]
                else:
                    # I guess it was just the end
                    return [solution, self.goal]
            if len(utils.squash(solution)) == self.max_len:  # the length checks out
                # It's a passible solution
                return [solution, self.goal]
            choiceOligo = np.random.choice(self.oligo, p=choiceWeights)
            choice = self.oligo.index(choiceOligo)
            overlap = utils.check_overlap(
                self.oligo[currIndex], self.oligo[choice])+1
            self.pheromones[currIndex][choice] /= 2
            for i in range(0, len(self.oligo)):
                weights[currIndex][i] = self.pheromones[currIndex][i] / sum(self.pheromones[currIndex])
            currLen += overlap
            solution.append(self.oligo[choice])
            self.goal = self._goal_function(solution)
            currIndex = choice
            

    def _generate_solutions(self):
        solutions = []
        for _ in range(0, self.colony_size):
            solutions.append(self._generate_solution(self.pheromones))
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
                if (self.pheromones[i][j] != 0):
                    self.pheromones[i][j] = self.pheromones[i][j]**self.alpha * self.spect_graph[i][j]**self.beta
                else:
                    self.pheromones[i][j] = 0.1**self.alpha * self.spect_graph[i][j]**self.beta

        currIndex = 0
        nextIndex = 0
        for result in topTen:
            result = result[0]
            for i in range(len(result)-1):
                currIndex = self.oligo.index(result[i])
                nextIndex = self.oligo.index(result[i+1])
                self.pheromones[currIndex][nextIndex] += self.max_len / \
                    utils.check_overlap(result[i], result[i+1])

        # print(self.pheromones)

    def run(self):
        i = 0
        while (i < self.generations):
            print('generation: ', i+1)
            solutions = self._generate_solutions()
            self._compare_solutions(solutions)
            print("goal: ", self.topTen[0][-1])

            self._pheromone_update(self.topTen)

            i += 1
        #print(self.pheromones)
        return self.topTen


if __name__ == "__main__":
    pass
