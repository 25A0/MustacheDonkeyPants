import pytest

from mdpants import mdpants
import argparse
import binascii

# Test that parse_args fails when mandatory elements are missing
def test_fails_without_arguments():
    with pytest.raises(SystemExit):
        mdpants.parse_args([])

def test_just_random_succesds():
    assert mdpants.parse_args(['-R'])

def test_single_file_succesds():
    assert mdpants.parse_args(['existing_file'])

def test_random_and_file_fails():
    with pytest.raises(SystemExit):
        assert mdpants.parse_args(['-R', 'existing_file'])

def test_infile_and_binary_fails():
    with pytest.raises(SystemExit):
        assert mdpants.parse_args(['--in existing_file', '--bin existing_file'])

def test_infile_needs_argument():
    with pytest.raises(SystemExit):
        assert mdpants.parse_args(['--in'])

def test_binfile_needs_argument():
    with pytest.raises(SystemExit):
        assert mdpants.parse_args(['--bin'])

def test_word_count():
    assert mdpants.len_wordlist('tests/testwordlist.txt') == 50

def test_word_count_sparse():
    assert mdpants.len_wordlist('tests/testsparsewordlist.txt') == 50

def test_accept_lines_with_not_only_whitespace():
    assert mdpants.accept_line(' foo \n')
    assert mdpants.accept_line('foo\n')
    assert mdpants.accept_line('\t\tfoo\t\n')

def test_seed_depends_on_file_content():
    seed1 = mdpants.get_hash_seed('tests/existing_file')
    seed2 = mdpants.get_hash_seed('tests/another_existing_file')
    assert seed1 <> seed2

def test_seed_deterministic():
    seed1 = mdpants.get_hash_seed('tests/existing_file')
    seed2 = mdpants.get_hash_seed('tests/existing_file')
    assert seed1 == seed2

    seed3 = binascii.unhexlify('0cf9180a764aba863a67b6d72f0918bc131c6772642cb2dce5a34f0a702f9470ddc2bf125c12198b1995c233c34b4afd346c54a2334c350a948a51b6e8b4e6b6')
    assert seed3 == seed1

def test_random_seed_not_trivially_broken():
    seed1 = mdpants.get_prng_seed()
    seed2 = mdpants.get_prng_seed()
    assert seed1 <> seed2

def test_extract_words():
    count = mdpants.len_wordlist('tests/testwordlist.txt')
    words = mdpants.fetch_words('tests/testwordlist.txt',
        [0.0/count, 1.0/count, 2.0/count], 'text')
    assert words == ['Aa', 'Aaa', 'Aah']

def test_extract_sparse_words():
    count = mdpants.len_wordlist('tests/testsparsewordlist.txt')
    words = mdpants.fetch_words('tests/testsparsewordlist.txt',
        [0.0/count, 4.0/count, 22.0/count], 'text')
    assert words == ['Aa', 'Aahing', 'Aasvogels']


