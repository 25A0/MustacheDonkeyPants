
all: words.bin emoticons.bin

%.bin: %.txt
	./mdpants/constant_width.py -o $@ $^

clean:
	rm *.bin

test:
	python -m pytest tests/test_mdpants.py
	python -m pytest tests/test_constant_width.py
