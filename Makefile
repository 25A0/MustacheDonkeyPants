BINLISTS := $(addsuffix .bin, $(basename $(wildcard mdpants/lists/*.txt)))
VERSION := $(shell cat mdpants/version)
DISTFILES = dist/mdpants-${VERSION}*

.PHONY: test clean dist_test all dist

default:
	@echo 'no default rule'

%.bin: %.txt
	./mdpants/constant_width.py -o $@ $^

clean:
	rm mdpants/lists/*.bin
	rm -rf dist/*
	python setup.py develop --uninstall

test: ${BINLISTS}
	python -m pytest tests

dist-test: test
	python setup.py sdist test

dev:
	python setup.py develop

virtenv:
	virtualenv virtenv

test-dist: dist virtenv $(addprefix test-dist-, $(notdir $(shell echo $(DISTFILES))))

test-dist-%: dist
	. virtenv/bin/activate ;\
	pip install dist/$* ;\
	cd virtenv ;\
	which mdpants ;\
	echo 'Hello World!' | bin/mdpants - ;\
	deactivate ;\
	virtualenv --clear virtenv

test-publish:
	python setup.py register -r https://testpypi.python.org/pypi
	python setup.py upload -r https://testpypi.python.org/pypi

dist: ${BINLISTS} mdpants/*.py tests/*.py setup.py
	python setup.py sdist
	python setup.py bdist_wheel
