import utils

# dummy function
@utils.timing_decorator
def f(a):
    for _ in range(a):
        i = 0
    return -1

if __name__ == "__main__":
    # dna = utils.read_dna_from_file('data/sequence.txt')
    # dna = utils.write_dna_to_file('ACGGTCGA','data/sequence.txt')
    dna = utils.generate_dna(n=1000)
    dna_cut = utils.cut_dna(dna, 4)
    print(dna_cut)
    # dna = utils.generate_all_combinations(5)
    # f(100000000)

    utils.generate_repetitions(dna_cut)