#!/usr/bin/env python

import sys
from io import open, DEFAULT_BUFFER_SIZE
import argparse
import hashlib
import os
from os import path
import binascii
import numpy
import codecs
import struct

from pkg_resources import resource_filename

DEFAULT_N_WORDS = 3

def get_hash_seed(filename):
    hash_alg = hashlib.sha512()
    if filename.strip() is '-':
        f = sys.stdin
    else: 
        f = codecs.open(filename, 'rb')

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

def get_seed(file=None):
    if file is None:
        return get_prng_seed()
    else:
        return get_hash_seed(file)

def len_wordlist(filename):
    count = 0
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if accept_line(line):
                count +=1
    return count

def postprocess(word):
    return word.strip().title()

def accept_line(line):
    return len(line.strip()) > 0

def fetch_text(filename, sorted_float_indices):
    total = len_wordlist(filename)
    sorted_indices = [int(x * total) for x in sorted_float_indices]
    count = 0
    sorted_words = []
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if not accept_line(line):
                continue
            if len(sorted_indices) is 0:
                break
            # We use a while loop instead of a simple check since there might
            # be cases where the same index appears multiple times
            while len(sorted_indices) > 0 and count == sorted_indices[0]:
                sorted_words.append(postprocess(line))
                del sorted_indices[0]
            count += 1
    return sorted_words

def fetch_binary(filename, sorted_float_indices):
    sorted_words = []
    with open(filename, 'br') as f:
        count = int(struct.unpack('=q', f.read(8))[0])
        max_line = int(struct.unpack('=q', f.read(8))[0])
        sorted_indices = [int(x * count) for x in sorted_float_indices]
        current = sorted_indices[0]
        advance = current
        while len(sorted_indices) > 0:
            f.seek(max_line*advance, os.SEEK_CUR)
            current = sorted_indices[0]

            bin_word = f.read(max_line)
            word = bin_word[:bin_word.index(b'\x0a')].decode('utf-8')
            sorted_words.append(postprocess(word))
            del sorted_indices[0]
            if len(sorted_indices) == 0: break

            # The # of bytes that we need to advance is the distance between
            # the current position and the position of the next index
            advance = sorted_indices[0] - (current + 1)
    return sorted_words

def fetch_words(filename, indices, mode):
    if len(indices) == 0: return []
    sorted_indices = sorted(indices)

    if mode is 'binary':
        sorted_words = fetch_binary(filename, sorted_indices)
    elif mode is 'text':
        sorted_words = fetch_text(filename, sorted_indices)

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
        usage='%(prog)s [-N n] [-c char] [--(in|bin) <file>] [-R|-|<file>]')
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

    word_input = parser.add_mutually_exclusive_group()
    word_input.add_argument('--in',
        dest='in', metavar='<file>',
        help='Use the words from the specified text file (default: %(default)s).')
    word_input.add_argument('--bin',
        dest='bin', metavar='<file>',
        help='Use the words from the specified binary file (see constant_width.py).')

    parser.add_argument('-c', '--concat',
        dest='concat', metavar='char', default='.',
        help='Use the specified character or string to concatenate the words (default: %(default)s).')

    parser.add_argument('--emoticons', 
        dest='emoticons', action='store_true',
        help='Use a small set of emoticons instead of words.')

    return parser.parse_args(arguments)

def get_indices(seed, count):
    numpy.random.seed(bytearray(seed))
    return numpy.random.rand(count)

def main(argv = None):
    if argv == None:
        # Starting at index 1 to skip the name of the program
        argv = sys.argv[1:]
    args = vars(parse_args(sys.argv[1:]))

    # Initialize the sequence that will determine which words are used
    seed = get_seed(args['file'])

    # If the user wants emoticons, pick the binary list of emoticons that
    # ships with the package
    if args['emoticons']:
        args['bin'] = resource_filename(__name__, 'lists/emoticons.bin')

    # If no list is specified, use default list
    if not (args['in'] or args['bin']):
        args['bin'] = resource_filename(__name__, 'lists/words.bin')

    if args['bin']:
        if not os.path.isfile(str(args['bin'])):
            print(args['bin'] + ": no such file or directory")
            sys.exit(2)
        mode = 'binary'
        wordlist_filename = args['bin']
    elif args['in']:
        if not os.path.isfile(str(args['in'])):
            print(args['in'] + ": no such file or directory")
            sys.exit(2)
        mode = 'text'
        wordlist_filename = args['in']
    else:
        print("Use --in or --bin to specify a word list.")
        sys.exit(2)

    # These indices are floats in [0, 1) and will later be translated into
    # integers within the limits of the word list.
    indices = get_indices(seed, args['num_words'])
    words = fetch_words(wordlist_filename, indices, mode)

    print(args['concat'].join(words).encode('utf-8'))

    # print('# words in list: {}'.format(len_wordlist))
    # print('indices: {}'.format(indices))
    return 0


if __name__ == '__main__':
    sys.exit(main())
    