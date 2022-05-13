import utils

class AntColony:
    pass


if __name__ == "__main__":
    # dna = utils.read_dna_from_file('data/sequence.txt')
    # dna = utils.write_dna_to_file('ACGGTCGA','data/sequence.txt')
    dna = utils.generate_dna(n=20)
    dna_cut = utils.cut_dna(dna, 3)
    print(dna_cut)
    #pass