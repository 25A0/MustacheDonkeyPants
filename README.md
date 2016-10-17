## Mustache Donkey Pants

This is a small tool to generate a deterministic, pronounceable and memorable names for a given input.
Inspired by https://destructible.io/ and https://what3words.com/.

### Usage

```
	% echo 'Hello World!' > myfile
	% mdpants myfile
	MustacheDonkeyPants
```

The output depends on the file content, not the filename:	

```
	% echo 'Thanks for all the fish!' > myfile
	% mdpants myfile
	SomeOtherName
```

You can vary the number of words that the output is comprised of:

```
	% echo 'Hello World' > myfile
	% mdpants -n5 myfile
	MustacheDonkeyPantsPotatoeCar
```

### Words

The words used by this tool come from a curated version of the _"Single"_ word
list of the [Moby project](http://icon.shef.ac.uk/Moby/mwords.html). The original
list was released to the public domain in 1996, and contained 354,984 words.
The modified version used in this project contains `wc words.txt`.

## But... why?

Here's what I use this tool for: I often share files by putting them in a
folder on my server without access restriction. But I don't want people to be
able to see what else is lying around there. The content of that folder is not
enumerable, but people could still try to guess filenames. Using the hash of
the file as the filename would solve that, but those URLs would not be
pronounceable. With Mustache Donkey Pants I can easily generate unique,
memorable and pronounceable file names without having to worry about collisions
or people guessing URLs.
