import pytest

from mdpants import mdpants
from os import path

def test_dist_has_wordlist_txt():
	assert path.isfile("words.txt")

def test_dist_has_wordlist_bin():
	assert path.isfile("words.bin")

def test_dist_has_emoticons_txt():
	assert path.isfile("emoticons.txt")

def test_dist_has_emoticons_bin():
	assert path.isfile("emoticons.bin")
