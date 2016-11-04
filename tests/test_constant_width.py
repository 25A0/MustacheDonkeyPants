import pytest

import os
from mdpants import mdpants, constant_width
import binascii

def test_wordlist_stats():
    stats = constant_width.wordlist_stats('tests/lists/wordlist.txt')
    assert stats['count'] == 50
    assert stats['max_line'] == 12

def test_sparse_wordlist_stats():
    stats = constant_width.wordlist_stats('tests/lists/sparsewordlist.txt')
    assert stats['count'] == 50
    assert stats['max_line'] == 12

def test_rewrite():
    stats = constant_width.wordlist_stats('tests/lists/wordlist.txt')
    constant_width.rewrite('tests/lists/wordlist.txt', 'tests/lists/wordlist.bin', stats)

    seed = mdpants.get_seed()
    indices = mdpants.get_indices(seed, 3)

    text_words = mdpants.fetch_words('tests/lists/wordlist.txt', indices, 'text')
    binary_words = mdpants.fetch_words('tests/lists/wordlist.bin', indices, 'binary')

    assert text_words == binary_words

def test_rewrite_sparse():
    stats = constant_width.wordlist_stats('tests/lists/sparsewordlist.txt')
    constant_width.rewrite('tests/lists/sparsewordlist.txt', 'tests/lists/sparsewordlist.bin', stats)

    seed = mdpants.get_seed()
    indices = mdpants.get_indices(seed, 3)

    text_words = mdpants.fetch_words('tests/lists/sparsewordlist.txt', indices, 'text')
    binary_words = mdpants.fetch_words('tests/lists/sparsewordlist.bin', indices, 'binary')

    assert text_words == binary_words
