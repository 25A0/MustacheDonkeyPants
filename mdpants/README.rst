Mustache Donkey Pants
=====================

This is a small tool to generate deterministic, pronounceable and memorable words from a given input.
Inspired by https://destructible.io/ and https://what3words.com/.

Install
-------

::

    pip install mdpants

Or::

    git clone git@github.com:25A0/MustacheDonkeyPants.git
    python setup.py develop


Usage
-----

:: 

    % echo 'Hello World!' > myfile
    % mdpants myfile
    Plottage.Hypoazoturia.Congresswomen

The output depends on the file content, not the filename::

    % echo 'Thanks for all the fish!' > myfile
    % mdpants myfile
    Noncalculable.Cremationist.Somersetted
    % echo 'Thanks for all the fish!' | mdpants -
    Noncalculable.Cremationist.Somersetted


You can vary the number of words that the output is comprised of::

    % echo 'Hello World' > myfile
    % mdpants -N5 myfile
    Plottage.Hypoazoturia.Congresswomen.Affiliable.Specks

You can specify a different list of words if you want::

    % echo "foo\nbar\nbaz" > foolist
    % echo 'Hello World!' | mdpants --in foolist -
    Bar.Bar.Foo

It works with emoticons, too::

    % echo 'Hello World!' > myfile
    % mdpants --emoticons myfile
    😳.😟.😍

To change the delimiter between words, use the ``-c`` option::

    % echo 'Never gonna give you up' > myfile
    % mdpants -c ' - ' myfile
    Lings - Distractedness - Buhl

If you do want a result that is pseudorandomly generated, rather than
deterministically, use the ``-R`` flag::

    % mdpants -R
    Unplagiarized.Cytotropism.Ravelings
    % mdpants -R
    Bismuthous.Fizzwater.Maxicoats

Binary wordlists
----------------

Reading through more than 300,000 words can take a while. To speed things up,
run ``make`` to produce a more efficient version of the word list. Then run
mdpants with the ``--bin <file>`` option, like so::

    % echo 'Hello World' > myfile
    % mdpants --bin words.bin myfile

While the generation of the binary wordlist takes a while, and the resulting
file is quite a bit larger than the original file, you will find that mdpants
finishes much faster with the binary wordlists.

Words
=====

The words used by this tool come from a mildly curated version of the
_"Single"_ word list of the `Moby project`_. The original list was
released to the public domain in 1996, and contained 354,984 words. The
modified version used in this project contains `wc words.txt` words.

What I've changed compared to the original list:

- any line matching ``[^a-z\s]`` was removed
- any single-letter words were removed

Thus, all words contain only a-z and have a length of at least 2.

But... why?
===========

Here's what I will use this tool for: I often share files by putting them in a
folder on my server without access restriction. But I don't want people to be
able to see what else is lying around there. The content of that folder is not
enumerable, but people could still try to guess filenames. Using the hash of
the file as the filename would solve that, but those URLs would not be
pronounceable. With Mustache Donkey Pants I can easily generate unique,
memorable and pronounceable file names without having to worry about collisions
or people guessing URLs.

Disclaimer
==========

Although ``alias md5=mdpants --emoticons -N 16`` sounds like a great idea, you
really shouldn't use this as a sort of weird replacement for a hash function.

Final note
==========

I'll buy you a beer if you find the file that produces ``Mustache.Donkey.Pants``!

.. _Moby project: http://icon.shef.ac.uk/Moby/mwords.html