#!/usr/bin/env python

import sys
from io import open, DEFAULT_BUFFER_SIZE
import argparse
import hashlib
import os
import binascii
import numpy
import codecs
import struct

from mdpants import accept_line

def wordlist_stats(filename):
    '''
    Scan through the given file, counting the number of lines,
    and keeping track of the maximum line length
    '''
    count = 0
    max_line = 0
    total = 0
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if not accept_line(line):
                continue
            count +=1
            total += len(line)
            if _len_word(line) > max_line:
                max_line = _len_word(line)
    res = dict()
    res['count'] = count
    res['max_line'] = max_line
    res['total'] = total
    return res

def rewrite(infilename, outfilename, stats):
    new_total = 0
    if not outfilename:
        outfile = sys.stdout
    else:
        outfile = codecs.open(outfilename, 'w', encoding='utf-8')
    try:
        outfile.write(struct.pack('=q', stats['count']))
        outfile.write(struct.pack('=q', stats['max_line']))
        with codecs.open(infilename, 'r', encoding='utf-8') as f:
            for line in f:
                if not accept_line(line):
                    continue
                # Write the stripped line to outfile, append newline
                line = line.strip() + '\n'
                outfile.write(unicode(line))
                # Pad with 0 bytes until max_line bytes are reached
                rem = stats['max_line'] - _len_word(line)
                outfile.write(b'\x00'*rem)
    finally:
        outfile.close()
    stats['new_total'] = new_total

def _len_word(word):
    return len((word.strip() + '\n').encode('utf-8'))

def list_words(infilename):
    words = []
    with open(infilename, 'rb') as f:
        count = int(struct.unpack('=q', f.read(8))[0])
        print(count)
        max_line = int(struct.unpack('=q', f.read(8))[0])
        print(max_line)
        c = 0
        while c < count:
            word = f.read(max_line)
            words.append(word[:word.index(b'\x0a')].decode('utf-8'))
            c += 1

def get_word(infilename, index):
    with open(infilename, 'br') as f:
        count = int(struct.unpack('=q', f.read(8))[0])
        print(count)
        max_line = int(struct.unpack('=q', f.read(8))[0])
        print(max_line)
        f.seek(max_line*index, os.SEEK_CUR)
        word = f.read(max_line)
        word = word[:word.index(b'\x0a')].decode('utf-8')
    print(word.encode('utf-8'))

def fetch_words(filename, indices):
    if len(indices) == 0: return []
    count = 0
    sorted_words = []
    sorted_indices = sorted(indices)
    with open(filename, 'br') as f:
        count = int(struct.unpack('=q', f.read(8))[0])
        print(count)
        max_line = int(struct.unpack('=q', f.read(8))[0])
        print(max_line)
        advance = sorted_indices[0]
        while len(sorted_indices) > 0:
            f.seek(max_line*advance, os.SEEK_CUR)
            word = f.read(max_line)
            sorted_words.append(word[:word.index(b'\x0a')].decode('utf-8'))
            del sorted_indices[0]
            if len(sorted_indices) == 0: break

            # The # of bytes that we need to advance is the distance between
            # the current position and the position of the next index
            advance = sorted_indices[0] - (advance + 1)
        
    # Re-order the words so that they appear in the specified order, rather
    # than in the sorted order
    words = []
    sorted_indices = sorted(indices)
    for index in indices:
        words.append(sorted_words[sorted_indices.index(index)])
    return words

def parse_args(arguments):
    parser = argparse.ArgumentParser(
        description='''
        Convert a text file to a binary format such that each line in the file
        is padded to a constant width. This makes it easy to seek to a specific
        line in the file, since we can just calculate the offset at which the
        desired line starts.
        ''')

    parser.add_argument('file',
        help='The file that is converted. If - is specified, %(prog)s will read from stdin instead.')

    parser.add_argument('-o', '--out',
        dest='out', metavar='file',
        help='The output file. If it is not specified, %(prog)s will write to stdout instead.')

    return parser.parse_args(arguments)

if __name__ == '__main__':
    # Starting at index 1 to skip the name of the program
    args = vars(parse_args(sys.argv[1:]))

    stats = wordlist_stats(args['file'])
    print(stats)

    rewrite(args['file'], args['out'], stats)
