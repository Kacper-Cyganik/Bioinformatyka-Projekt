from random import choice
from functools import wraps
from time import time
import itertools
import numpy as np
import config

def squash(tab):
    result = tab[0]
    for i in range(0, len(tab)-1):
        oligo1 = tab[i]
        oligo2 = tab[i+1]
        matching = 0
        for j in range(0, len(oligo1)+1):
            finish = False
            for k in range(0, matching):
                end = oligo1[len(oligo1)-matching+k]
                start = oligo2[k]
                if (end != start):
                    finish = True
                    break
            if(finish):
                break
            matching += 1
        matching -= 1
        result += oligo2[matching:]
    return result

def timing_decorator(f):
    '''
    measures time of executing method 'f'
    '''
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        # print(f'func :{f.__name__} args:{args} took: {te-ts}')
        return result
    return wrap


def generate_dna(n: int) -> str:
    '''
    returns string containing of with a length of 'n'
    '''
    nucleotides = ('A', 'T', 'G', 'C')
    return ''.join(choice(nucleotides) for _ in range(n))


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


def generate_all_combinations(n: int) -> list:
    '''
    returns list of all possible sequences
    '''
    nucleotides = 'ACGT'
    output = list(itertools.product(nucleotides, repeat=n))
    return output


def generate_repetitions(data: dict):
    '''
    generate dict that contains repetitions of oligonucleotides
    '''
    output = {}
    my_sum = 0
    for i in data:
        x = data.count(i)
        output[i] = x if x < 3 else '*'

    for i in output:
        if output[i] != 1:
            my_sum += 1
    return my_sum, output


def include_errors(start_neg: int, dict_data: dict, n_positives: int, n_negitves: int, oligo_len: int) -> None:
    '''
    include positive and negative errors to dict_data
    '''
    # negatives
    negative_index = start_neg
    while negative_index < n_negitves:
        to_delete_index = choice(list(dict_data.keys()))
        if dict_data[to_delete_index] == 1:
            negative_index += 1
        dict_data.pop(to_delete_index)

    # positives
    positive_index = 0
    while positive_index < n_positives:
        new = generate_dna(oligo_len)
        if new not in dict_data.keys():
            dict_data[new] = 1  # być może losowo?
            positive_index += 1


def check_overlap(word1: str, word2: str) -> int:
    '''
    returns how many nucletides overlap (for example: check_overlap('ACTAGACT', 'CTAGACTG')->)
    '''
    if (word1 == word2):
        return len(word1)
    else:
        for i in range(1, len(word1)):
            newWord1 = word1[i:]
            newWord2 = word2[:len(word1)-i]
            if(newWord1 == newWord2):
                return i
        return len(word1)   


if __name__ == '__main__':
    print(check_overlap('ABCDEFGH', 'BCDEFGHY'))

def generate_graph(data: list):
    '''
    returns grap representation of given data
    '''
    n = len(data)
    # create NxN matrix of zeros
    graph = [[0 for x in range(n)] for y in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                overlap = check_overlap(data[i], data[j])
                if overlap <= 2:  # if overlap is big enough, add edge
                    graph[i][j] = config.N_DNA_CUT-overlap

    # for i in range(len(graph[0])):
    #     graph[i][i] = 999

    my_list = []
    # for row in graph:
    #     my_list +=row
    # print(set(my_list))

    return np.array(graph)


def hamming_distance(string1, string2):
    dist_counter = 0
    for n in range(len(string1)):
        if string1[n] != string2[n]:
            dist_counter += 1
    return dist_counter
