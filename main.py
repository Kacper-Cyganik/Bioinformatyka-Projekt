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
    # dna = utils.generate_dna(n=20)
    # dna_cut = utils.cut_dna(dna, 3)
    # print(dna_cut)
    f(100000000)