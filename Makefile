
all: words.bin emoticons.bin

%.bin: %.txt
	./src/constant_width.py -o $@ $^

clean:
	rm *.bin
