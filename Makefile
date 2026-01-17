.PHONY: init lint format test clean

init:
	uv sync

lint:
	uv run flake8 upkquake

format:
	uv run black .

test:
	uv run pytest -s tests --doctest-modules

clean:
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf .venv
	find . -name '__pycache__' -type d -exec rm -rf {} +

.DEFAULT_GOAL := init
