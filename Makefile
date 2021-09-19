init:
	poetry install

lint:
	poetry run flake8 upkquake

format:
	poetry run black .

test:
	poetry run pytest -s tests --doctest-modules

clean:
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -name '__pycache__' -type d -exec rm -rf {} +
