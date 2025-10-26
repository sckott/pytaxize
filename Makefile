.PHONY: test docs

install:
	uv pip install .

test:
	uv run pytest --verbose --record-mode=once --disable-warnings --cov=pytaxize/ test/

docs-build:
	uv sync --group docs && uv run mkdocs build

docs-serve:
	uv sync --group docs && uv run mkdocs serve

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
