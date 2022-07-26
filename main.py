import utils
from config import N_NEGATIVES, N_POSITIVES, N_DNA, N_DNA_CUT
from ant_colony import ACO

def main():

    # Generate DNA of length n
    dna = utils.generate_dna(n=N_DNA)

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
    aco = ACO()

    topTen = aco.run(graph, dna_out, initNodeIndex,
                       initNode, N_DNA, len(dna_cut))
    print('Ostateczne wyniki: ')
    print(topTen[0])
    print("------")

    # Print DNA
    print(dna)
    print(utils.squash(topTen[0][0]))


if __name__ == "__main__":
    main()
