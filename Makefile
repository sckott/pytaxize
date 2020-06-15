# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = docs/_build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


all: build install

.PHONY: build install test docs distclean dist upload

build:
	python3 setup.py build

install: build
	python3 setup.py install

test:
	pytest --verbose --disable-warnings --cov=pytaxize/ --ignore setup.py

docs:
	sphinx-build -b html docs/ docs/_build

check:
	python3 -m twine check dist/*

distclean:
	rm dist/*

dist:
	python3 setup.py sdist bdist_wheel --universal

register:
	python3 setup.py register

up:
	python3 -m twine upload dist/*

uptest:
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
