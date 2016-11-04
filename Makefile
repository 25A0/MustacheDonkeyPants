BINLISTS := $(addsuffix .bin, $(basename $(wildcard mdpants/lists/*.txt)))
VERSION := $(shell cat mdpants/version)
# The types of distributions we will produce
DISTTYPES = ".tar.gz -py2-none-any.whl"

.PHONY: test clean dist_test test-dist

default:
	@echo 'no default rule'

# Create binary (compressed) version of given txt file
%.bin: %.txt
	./mdpants/constant_width.py -o $@ $^

clean:
	rm mdpants/lists/*.bin
	rm -rf dist/*
	rm -rf build
	rm -rf *.egg-info
	rm -rf .eggs
	python setup.py develop --uninstall

# Run unit test
test: ${BINLISTS}
	python -m pytest tests

# Install package in develop mode
dev:
	python setup.py develop

# Set up virtual environment to test dist files
virtenv:
	virtualenv virtenv

# Check for all dist files if we can install them
test-dist: dist virtenv $(addprefix test-dist-mdpants-${VERSION}, $(notdir $(shell echo $(DISTTYPES))))

# Check for an individual dist file if we can install them in a virtual env
# Will be called as e.g. test-dist-mdpants-0.5.0.tar.gz
test-dist-%: dist
	. virtenv/bin/activate ;\
	pip install dist/$* ;\
	cd virtenv ;\
	which mdpants ;\
	echo 'Hello World!' | bin/mdpants - ;\
	deactivate ;\
	virtualenv --clear virtenv

# Check if we can install the package from pypi after publishing it
# This will only publish it to the pypi test server
test-pip-test: test-publish
	. virtenv/bin/activate ;\
	pip install -i https://testpypi.python.org/pypi mdpants ;\
	cd virtenv ;\
	which mdpants ;\
	echo 'Hello World!' | bin/mdpants - ;\
	deactivate ;\
	virtualenv --clear virtenv

# Upload dist files to the pypi test server
test-publish: dist
	twine upload -r pypitest dist/mdpants-${VERSION}*

# Build dist files
dist: $(addprefix dist/mdpants-${VERSION}, $(shell echo $(DISTTYPES)))

# Build source dist
dist/mdpants-${VERSION}%.tar.gz: ${BINLISTS} mdpants/* tests/* setup.py
	python setup.py sdist

# Build wheel
dist/mdpants-${VERSION}%.whl: ${BINLISTS} mdpants/* tests/* setup.py
	python setup.py bdist_wheel
