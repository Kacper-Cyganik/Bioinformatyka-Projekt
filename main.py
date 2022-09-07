import utils
from config import N_NEGATIVES, N_POSITIVES, N_DNA, N_DNA_CUT
from ant_colony import ACO
import Levenshtein

def main():


    # Generate DNA of length n
    dna = utils.generate_dna(n=N_DNA)
    #utils.write_dna_to_file(dna, 'data/dna500.txt')
    #dna = utils.read_dna_from_file('data/dna200.txt')
    # Cut DNA into k-length nucleotides
    dna_cut = utils.cut_dna(dna, N_DNA_CUT)
    my_sum, repetitions = utils.generate_repetitions(dna_cut)

    # Include errors
    negative_errors = int(N_DNA*N_NEGATIVES)
    positive_errors = int(N_DNA*N_POSITIVES)
    utils.include_errors(my_sum, repetitions,
                         positive_errors, negative_errors, N_DNA_CUT)

    # Sort nucleotides
    dna_out = sorted(list(repetitions.keys()))

    # Generate graph
    graph = utils.generate_graph(dna_out)

    # Create initial (starting) node
    initNode = dna_cut[0]
    initNodeIndex = 0
    for count, value in enumerate(dna_out):
        if(value == initNode):
            initNodeIndex = count

    # Run ACO
    aco = ACO(alpha=5, beta=5, colony_size=50, generations=10, evaporation_rate=0.4, spect_graph=graph,
              oligo=dna_out, init_node_index=initNodeIndex, init_node=initNode, max_len=N_DNA, spect_oligo=len(dna_cut), repetitions=repetitions)

    topTen = aco.run()
    print('Ostateczne wyniki: ')
    print(topTen[0])
    print("------")

    # Print DNA
    print('Original DNA')  
    print(dna)
    print('Found DNA')
    result = utils.squash(topTen[0][0])
    print(result)

    print(Levenshtein.distance(dna, result))

if __name__ == "__main__":
    main()
