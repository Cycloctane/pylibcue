CC = gcc
LEX = flex
YACC = bison
PYTHON = python3
LIBCUE = vendor/libcue


$(LIBCUE)/cue_scanner.c:
	$(LEX) -o $@ $(LIBCUE)/cue_scanner.l

$(LIBCUE)/cue_parser.c $(LIBCUE)/cue_parser.h:
	$(YACC) -l -d -o $(firstword $@) $(LIBCUE)/cue_parser.y

parser: $(LIBCUE)/cue_scanner.c $(LIBCUE)/cue_parser.c $(LIBCUE)/cue_parser.h

ext: parser
	$(PYTHON) setup.py build_ext --inplace
