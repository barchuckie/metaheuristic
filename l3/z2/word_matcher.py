"""Word matcher

Module to calculate fitness function and performing mutations and recombinations of words.
"""
import random


def fitness_function(m, word):
    """Calculate fitness of the word using multiset.

    - m -- multiset of chars with their possible number of occurrences and points
    - word -- word to calculate fitness of
    """
    result = 0
    multiset = copy_multiset(m)
    for char in word:
        if char not in multiset.keys():
            return -1
        entry = multiset[char]
        result += entry['value']
        entry['count'] -= 1
        if entry['count'] <= 0:
            del multiset[char]
    return result


def copy_multiset(multiset):
    """Copy multiset.

    Multiset is a dict of dicts with chars as keys.
    Lower dicts under chars stores their number of occurrences and their points.
    """
    multiset_copy = {}
    for k, e in multiset.items():
        multiset_copy[k] = e.copy()
    return multiset_copy


class WordMatcher:
    """Class for manipulating words from a dictionary (Trie)."""

    def __init__(self, dictionary):
        """Create new instance with a dictionary."""
        self.dictionary = dictionary

    def fitness(self, element):
        """Calculate and return fitness of the element.

        Fitness is calculated as sum of points of chars in the element.
        If the element consist of unacceptable chars, then its fitness is -1.
        """
        fitness = self.dictionary.find(element)
        return fitness if fitness is not None else -1

    def recombine(self, parent1, parent2):
        """Recombine two parents to create their child word."""
        return parent1

    def mutate(self, word):
        """Mutate the word.

        A word is mutated by changing its random length suffix.
        """
        return self.dictionary.find_random_from_prefix(word[:random.randrange(len(word))])
