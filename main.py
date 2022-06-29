import utils
from config import N_NEGATIVES, N_POSITIVES, N_DNA, N_DNA_CUT
from ant_colony import AntColony
# dummy function
@utils.timing_decorator
def f(a):
    for _ in range(a):
        i = 0
    return -1

if __name__ == "__main__":
    # dna = utils.read_dna_from_file('data/sequence.txt')
    # dna = utils.write_dna_to_file('ACGGTCGA','data/sequence.txt')

    # generate DNA of n legnth
    dna = utils.generate_dna(n=N_DNA)

    # 
    dna_cut = utils.cut_dna(dna, N_DNA_CUT)

    my_sum, repetitions = utils.generate_repetitions(dna_cut)

    negative_errors = int(N_DNA*N_NEGATIVES)
    positive_errors  = int(N_DNA*N_POSITIVES)
    #print(negative_errors, positive_errors)

    utils.include_errors(my_sum, repetitions, positive_errors, negative_errors, N_DNA_CUT)
    dna_out = sorted(list(repetitions.keys()))

    #print('-----------')
    #print(dna_out)
    #print('-----------')
    #print(utils.generate_graph(dna_out))
    graph = utils.generate_graph(dna_out)
    #print(graph)
    # import numpy
    # with numpy.printoptions(threshold=numpy.inf):
    #     print(graph)
    import numpy as np
    #print(graph)
    # graph = np.array([[np.inf, 2, 2, 5, 7],
    #                   [2, np.inf, 4, 8, 2],
    #                   [2, 4, np.inf, 1, 3],
    #                   [5, 8, 1, np.inf, 2],
    #                   [7, 2, 3, 2, np.inf]])
    # print('----------------')
    # print(graph)

    ant_colony = AntColony(graph, 1, 1, 100, 0.95, alpha=1, beta=1)
    shortest_path = ant_colony.run()
    for i in shortest_path:
        print(i)

    utils.find_sequence_in_graph(shortest_path, graph, dna_out)
    #print ("shorted_path: {}".format(shortest_path))