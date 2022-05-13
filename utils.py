import random


def generate_dna(n: int) -> str:
    '''
    returns string containing of  with a length of 'n'
    '''
    nucleotides = ('A', 'T', 'G', 'C')
    return ''.join(random.choice(nucleotides) for i in range(n))


def write_dna_to_file(data: str, path: str):
    '''
    writes single string to file
    '''
    with open(path, 'w') as f:
        f.write(str(data))


def read_dna_from_file(path: str) -> str:
    '''
    reads single string from file
    '''
    with open(path, 'r') as f:
        return f.read()
