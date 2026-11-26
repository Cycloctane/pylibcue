LEX = flex
YACC = bison
PYTHON ?= python3
LIBCUE ?= vendor/libcue

.PHONY: parser ext test sdist wheel wheel-abi3 clean all

default: all

$(LIBCUE)/cue_scanner.c: $(LIBCUE)/cue_scanner.l
	$(LEX) --nounistd -o $@ $^

$(LIBCUE)/cue_parser.c $(LIBCUE)/cue_parser.h: $(LIBCUE)/cue_parser.y
	$(YACC) -l -d -o $(firstword $@) $^

parser: $(LIBCUE)/cue_scanner.c $(LIBCUE)/cue_parser.c $(LIBCUE)/cue_parser.h

ext: parser
	LIBCUE_PATH=$(LIBCUE) CC=$(CC) $(PYTHON) setup.py build_ext --inplace

test: ext
	$(PYTHON) -m unittest discover -v -s tests

sdist: parser
	$(PYTHON) -m build --sdist

wheel-abi3: export PYLIBCUE_LIMITED_API = 1

wheel wheel-abi3: parser
	LIBCUE_PATH=$(LIBCUE) CC=$(CC) $(PYTHON) -m build --wheel

all: sdist wheel

clean:
	rm -f pylibcue/*.so pylibcue/*.c
	rm -f $(LIBCUE)/cue_scanner.c $(LIBCUE)/cue_parser.c $(LIBCUE)/cue_parser.h
	rm -f dist/* wheelhouse/*
	rm -rf build/* *.egg-info
