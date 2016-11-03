
.PHONY: test clean dist_test all

all: words.bin emoticons.bin

%.bin: %.txt
	./mdpants/constant_width.py -o $@ $^

clean:
	rm *.bin
	rm -rf .eggs

test: words.bin emoticons.bin
	python -m pytest tests

dist_test: test
	python setup.py test
