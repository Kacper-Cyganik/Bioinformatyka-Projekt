import utils
from config import N_NEGATIVES, N_POSITIVES, N_DNA, N_DNA_CUT
from ant_colony import antColony



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

    graph = utils.generate_graph(dna_out)
    
    initNode = dna_out[0]
    initNodeIndex = 0
    for count, value in enumerate(dna_out):
        if(value == initNode):
            initNodeIndex = count
        
    

    
    # ant_colony = AntColony(graph, 1, 1, 100, 0.95, alpha=1, beta=1)
    # shortest_path = ant_colony.run()

    # utils.find_sequence_in_graph(shortest_path, graph, dna_out)
    # #print ("shorted_path: {}".format(shortest_path))