#!/usr/bin/env python

import sys
from io import open, DEFAULT_BUFFER_SIZE
import argparse
import hashlib
import os
import binascii
import numpy
import codecs

DEFAULT_N_WORDS = 3
VERSION = '0.1'

def get_hash_seed(filename):
    hash_alg = hashlib.sha512()
    if filename.strip() is '-':
        f = sys.stdin
    else: 
        f = codecs.open(filename, 'r', encoding='utf-8')

    try:
        s = f.read(DEFAULT_BUFFER_SIZE)
        while len(s) > 0:
            hash_alg.update(s)
            s = f.read(DEFAULT_BUFFER_SIZE)
        return hash_alg.digest()
    finally:
        f.close()


def get_prng_seed():
    # To simplify things, we'll generate the same amount of data as sha512
    return os.urandom(512/8)

def get_seed(file):
    if file is None:
        return get_prng_seed()
    else:
        return get_hash_seed(file)

def len_wordlist(filename):
    count = 0
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            count +=1
    return count

def postprocess(word):
    return word.strip().title().encode('utf-8')

def fetch_words(filename, indices):
    count = 0
    sorted_words = []
    sorted_indices = sorted(indices)
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if len(sorted_indices) is 0:
                break
            # We use a while loop instead of a simple check since there might
            # be cases where the same index appears multiple times
            while len(sorted_indices) > 0 and count == sorted_indices[0]:
                sorted_words.append(postprocess(line))
                del sorted_indices[0]
            count += 1

    # Re-order the words so that they appear in the specified order, rather
    # than in the sorted order
    words = []
    sorted_indices = sorted(indices)
    for index in indices:
        words.append(sorted_words[sorted_indices.index(index)])
    return words

def parse_args(arguments):
    def positive(string):
        val = int(string)
        if val <= 0:
            msg = 'The number of words needs to be positive.'
            raise argparse.ArgumentTypeError(msg)
        else: return val

    parser = argparse.ArgumentParser(
        description='Generate a deterministic, pronounceable and memorable set of words for a given input.',
        usage='%(prog)s [-N n] [-c char] [--in <file>] [-R|-|<file>]')
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('file',
        nargs='?',
        help='Use the content of this file to determine the output. If - is specified, %(prog)s will read from stdin instead.')
    group.add_argument('-R', '--random', 
        dest='random', action='store_true',
        help='Generate a pseudo-random output, rather than a deterministic one. The input file will be ignored in this case.')

    parser.add_argument('-N', '--number', 
        dest='num_words', metavar='num', type=positive,
        help='Set the number of words in the output (default: %(default)s).', 
        default=DEFAULT_N_WORDS)
    parser.add_argument('--in',
        dest='in', metavar='<file>', default='words.txt', 
        help='Use the words from the specified text file.')
    parser.add_argument('-c', '--concat',
        dest='concat', metavar='char', default='.',
        help='Use the specified character or string to concatenate the words (default: %(default)s).')
    # parser.add_argument('--bin',
    #     dest='bin', metavar='<file>',
    #     help='Use the words from the specified binary file.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(VERSION))
    return parser.parse_args(arguments)

if __name__ == '__main__':
    # Starting at index 1 to skip the name of the program
    args = vars(parse_args(sys.argv[1:]))
    # print(args)

    # Initialize the sequence that will determine which words are used
    seed = get_seed(args['file'])
    numpy.random.seed(bytearray(seed))

    len_wordlist = len_wordlist(args['in'])

    indices = [int(x * len_wordlist) for x in numpy.random.rand(args['num_words'])]

    words = fetch_words(args['in'], indices)

    print(args['concat'].join(words))

    # print('# words in list: {}'.format(len_wordlist))
    # print('indices: {}'.format(indices))


    