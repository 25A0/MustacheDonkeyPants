import pytest

import os
from mdpants import mdpants, constant_width
import binascii

def test_wordlist_stats():
    stats = constant_width.wordlist_stats('tests/testwordlist.txt')
    assert stats['count'] == 50
    assert stats['max_line'] == 12

def test_sparse_wordlist_stats():
    stats = constant_width.wordlist_stats('tests/testsparsewordlist.txt')
    assert stats['count'] == 50
    assert stats['max_line'] == 12

def test_rewrite():
    stats = constant_width.wordlist_stats('tests/testwordlist.txt')
    constant_width.rewrite('tests/testwordlist.txt', 'tests/testwordlist.bin', stats)

    seed = mdpants.get_seed()
    indices = mdpants.get_indices(seed, 3)

    text_words = mdpants.fetch_words('tests/testwordlist.txt', indices, 'text')
    binary_words = mdpants.fetch_words('tests/testwordlist.bin', indices, 'binary')

    assert text_words == binary_words

def test_rewrite_sparse():
    stats = constant_width.wordlist_stats('tests/testsparsewordlist.txt')
    constant_width.rewrite('tests/testsparsewordlist.txt', 'tests/testsparsewordlist.bin', stats)

    seed = mdpants.get_seed()
    indices = mdpants.get_indices(seed, 3)

    text_words = mdpants.fetch_words('tests/testsparsewordlist.txt', indices, 'text')
    binary_words = mdpants.fetch_words('tests/testsparsewordlist.bin', indices, 'binary')

    assert text_words == binary_words
