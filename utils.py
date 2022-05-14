from random import choice
from textwrap import wrap
from functools import wraps
from time import time
import itertools


def generate_dna(n: int) -> str:
    '''
    returns string containing of with a length of 'n'
    '''
    nucleotides = ('A', 'T', 'G', 'C')
    return ''.join(choice(nucleotides) for i in range(n))


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


def cut_dna(dna: str, k: int) -> list:
    '''
    returns list of substrings with a length of 'k' from single string
    '''
    # index = 0
    # while index < 
    return [dna[i: j] for i in range(len(dna)) for j in range(i + 1, len(dna) + 1) if len(dna[i:j]) == k]




def timing_decorator(f):
    '''
    measures time of executing method 'f'
    '''
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f'func :{f.__name__} args:{args} took: {te-ts}')
        return result
    return wrap


def generate_all_combinations(n: int) -> list:
    '''
    returns list of all possible sequences
    '''
    nucleotides = 'ACGT'
    output = list(itertools.product(nucleotides, repeat=n))
    return output


def generate_repetitions(data) -> dict():
    output = {}
    my_sum = 0
    for i in data:
        x = data.count(i)
        output[i]= x if x<3 else '*' 

    for i in output:
        if output[i] != 1:
            my_sum += 1
    return my_sum, output

def include_errors(dict_data, n_positives, n_negitves):

    # negatives
    negative_index = 0
    while negative_index < n_negitves:
        dict_data.remove()

