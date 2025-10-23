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

.PHONY: install test docs

install:
	uv pip install .

test:
	uv run pytest --verbose --disable-warnings --cov=pytaxize/ --ignore setup.py

docs:
	sphinx-build -b html docs/ docs/_build

check:
	uv run python -m twine check dist/*

distclean:
	rm dist/*

dist:
	uv run python setup.py sdist bdist_wheel --universal

register:
	python3 setup.py register

up:
	python3 -m twine upload dist/*

uptest:
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

lint-fix:
	uv run ruff check --select I --fix pytaxize

lint-check:
	uv run ruff check pytaxize

format-check:
	uv run ruff format --check pytaxize

format-fix:
	uv run ruff format pytaxize

ipython:
	uv run --with rich --with ipython python -m IPython

py:
	uv run python
