import pytest

from mdpants import mdpants
from os import path

from pkg_resources import resource_exists

def test_dist_has_wordlist_txt():
	assert resource_exists('mdpants', 'lists/words.txt')

def test_dist_has_wordlist_bin():
	assert resource_exists('mdpants', 'lists/words.bin')

def test_dist_has_emoticons_txt():
	assert resource_exists('mdpants', 'lists/emoticons.txt')

def test_dist_has_emoticons_bin():
	assert resource_exists('mdpants', 'lists/emoticons.bin')
