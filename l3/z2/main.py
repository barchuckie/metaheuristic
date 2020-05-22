"""L3/Z2.

Find the best matching word from dictionary with multiset of chars and their points
to calculate words scores. Searching is performed by Genetic Algorithm
with maximising the function of score.

Author: Patryk Barczak
"""
import os
import sys
import time

from genetic import GeneticAlgorithm
from trie import Trie
from word_matcher import WordMatcher


dirname = os.path.dirname(__file__)
DICT_FILENAME = os.path.join(dirname, 'dict.txt')


def read_dict(multiset):
    """Read words from dictionary file into the Trie.

    Words are inserted into the Trie only if they are made of chars from multiset.
    - multiset -- multiset of chars with number of their possible occurrences and points
    """
    trie = Trie(multiset)
    with open(DICT_FILENAME, 'r') as file:
        word = file.readline()
        while word:
            trie.insert(word.replace('\n', '').lower())
            word = file.readline()
    return trie


def find_best_match():
    """Find the best matching word from the dictionary."""
    i = input().split()
    time_limit = int(i[0])
    letter_multiset_size = int(i[1])
    initial_size = int(i[2])
    multiset = {}
    initial_words = []
    start_time = time.time()

    for _ in range(letter_multiset_size):
        e = input().split()
        if e[0] in multiset.keys():
            multiset[e[0]]['count'] += 1
        else:
            multiset[e[0]] = {'count': 1, 'value': int(e[1])}

    for _ in range(initial_size):
        initial_words.append(input().replace('\r', ''))

    trie = read_dict(multiset)
    matcher = WordMatcher(trie)
    genetic = GeneticAlgorithm(matcher)

    preprocessing_time = time.time() - start_time
    result = genetic.search(time_limit - preprocessing_time, initial_words)

    print(result, file=sys.stderr)
    print(matcher.fitness(result))


if __name__ == '__main__':
    find_best_match()
