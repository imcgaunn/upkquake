init:
	pip3 install -r requirements-dev.txt

lint:
	flake8 upkquake

format:
	black .

test:
	pytest -s tests --doctest-modules

install:
	pip install .

develop:
	pip install -e .

clean:
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -name '__pycache__' -type d -exec rm -rf {} +
