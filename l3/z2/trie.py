"""Trie module

This module implements trie (prefix tree) data structure to store words.
"""
import random
from typing import Dict

from word_matcher import fitness_function


class Node:
    """Single tree node representation."""

    def __init__(self):
        """Create new instance of node with empty children dict and None value."""
        self.children: Dict[str, Node] = {}
        self.value = None


def find(node, key):
    """Find key in the structure.

    I key is found then its value is returned, otherwise it returns None.
    """
    for char in key:
        if char in node.children:
            node = node.children[char]
        else:
            return None
    return node.value


def insert(node, key, value):
    """Insert key into the structure.

    Insert key and assign value to this.
    """
    for char in key:
        if char not in node.children:
            node.children[char] = Node()
        node = node.children[char]
    node.value = value


class Trie:
    """Class representing Trie data structure."""

    def __init__(self, multiset):
        """Initialize with a given multiset and new root node.

        - multiset -- set to calculate fitness (values) of the words
        """
        self.multiset = multiset
        self.root = Node()

    def find(self, key):
        """Find key in the trie."""
        return find(self.root, key)

    def insert(self, key):
        """Insert key into the trie.

        If key is not acceptable by multiset (fitness function returns -1),
        then it is ignored and not inserted.
        """
        value = fitness_function(self.multiset, key)
        if value < 0:
            return
        insert(self.root, key, value)

    def find_random_from_prefix(self, prefix):
        """Find random suffix for the given prefix.

        Walk the trie by prefix key and then randomly chose children until
        the created word cannot be longer.
        """
        node = self.root
        for char in prefix:
            assert char in node.children.keys()
            node = node.children[char]
        word = prefix
        while node.children:
            char, node = random.choice(list(node.children.items()))
            word += char
        return word

    def __str__(self):
        return f"{self.root.children.keys()}"
