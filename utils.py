from random import choice
import numpy as np
import config


def squash(arr: list) -> str:
    """Generates string from list of nucleotides excluding overlaping sequences

    Args:
        arr (list): list of k-length nucleotides

    Returns:
        str: string created from list of nucleotides.
    """
    result = arr[0]
    oligosize = len(arr[0])
    for i in range(0, len(arr)-1):
        oligo1 = arr[i]
        oligo2 = arr[i+1]
        if oligo1 == oligo2:
            result += oligo2
        else:
            for j in range(oligosize-1, 0, -1):
                if oligo1[oligosize-j:] == oligo2[:j]:
                    result += oligo2[j:]
                    break
    return result

    """result = arr[0]
    for i in range(0, len(arr)-1):
        oligo1 = arr[i]
        oligo2 = arr[i+1]
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
    return result, matching"""


def generate_dna(n: int) -> str:
    """Returns string containing of with a length of 'n'

    Args:
        n (int): length of final DNA sequence

    Returns:
        str: string containing of with a length of 'n'
    """
    nucleotides = ('A', 'T', 'G', 'C')
    return ''.join(choice(nucleotides) for _ in range(n))


def write_dna_to_file(data: str, path: str) -> None:
    """Writes single string to file

    Args:
        data (str): string
        path (str): path to file
    """
    with open(path, 'w') as f:
        f.write(str(data))


def read_dna_from_file(path: str) -> str:
    """Reads single string to file

    Args:
        data (str): string
        path (str): path to file
    """
    with open(path, 'r') as f:
        return f.read()


def cut_dna(dna: str, k: int) -> list:
    """Generates list of substrings with a length of 'k' from single string

    Args:
        dna (str): DNA sequence to cut
        k (int): length of each nucleotide

    Returns:
        list: list of nucleotides created from dna
    """
    return [dna[i: j] for i in range(len(dna)) for j in range(i + 1, len(dna) + 1) if len(dna[i:j]) == k]


# def generate_all_combinations(n: int) -> list:
#     """Creates list of all possible sequences

#     Args:
#         n (int):

#     Returns:
#         list: _description_
#     """
#     nucleotides = 'ACGT'
#     output = list(itertools.product(nucleotides, repeat=n))
#     return output


def generate_repetitions(data: list) -> tuple:
    """Calculate number of repetitions of each nucleotide in given list

    Args:
        data (list): list of nucleotides 

    Returns:
        my_sum (int): number of nucleotides where negative errors occur
        output (dict): dict containing nucleotide as key and number of its repetitions as value
    """
    '''
    '''
    output = {}
    my_sum = 0
    for i in data:
        x = data.count(i)
        output[i] = x if x < 5 else '*'

    for i in output:
        if output[i] != 1:
            my_sum += 1
    return my_sum, output


def include_errors(start_neg: int, dict_data: dict, n_positives: int, n_negitves: int, oligo_len: int) -> None:
    """Include positive and negative errors
    Args:
        start_neg (int): initial number of negative errors
        dict_data (dict): dictionary containing nucleotides with its number of repetitions
        n_positives (int): desired number of positive errors in output data
        n_negitves (int): desired number of positive errors in output data
        oligo_len (int): length of each nucleotide 
    """
    
    # negative errors
    negative_index = start_neg
    while negative_index < n_negitves:
        to_delete_index = choice(list(dict_data.keys()))
        if dict_data[to_delete_index] == 1:
            negative_index += 1
        dict_data.pop(to_delete_index)

    # positive errors
    positive_index = 0
    while positive_index < n_positives:
        new = generate_dna(oligo_len)
        if new not in dict_data.keys():
            dict_data[new] = 1  # być może losowo?
            positive_index += 1


def check_overlap(word1: str, word2: str) -> int:
    """Calculates how many nucleotides DOES NOT overlap (for example: check_overlap('ABCDEFGH', 'BCDEFGHY')->1)

    Args:
        word1 (str): first word to compare
        word2 (str): second word to compare

    Returns:
        int: number of NOT OVERLAPING chars
    """
    '''
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


def generate_graph(data: list):
    """Generate graph represented as 2d matrix 

    Args:
        data (list): 2d list of integers

    Returns:
        _type_: graph created from data
    """
    n = len(data)

    # create NxN matrix of zeros
    graph = [[0 for x in range(n)] for y in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                overlap = check_overlap(data[i], data[j])
                if overlap <= 3:  # if overlap is big enough, add edge
                    graph[i][j] = config.N_DNA_CUT-overlap
    return np.array(graph)


if __name__ == '__main__':
    print("AATTCCGCTC\n" + squash(['AATTCCGC', 'TTCCGCTC']))
