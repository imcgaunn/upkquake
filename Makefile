init:
	pip3 install -r requirements-dev.txt

lint:
	flake8 upkquake

test:
	pytest -s upkquake --doctest-modules

install:
	python setup.py install

develop:
	pip install -e .

clean:
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -name '__pycache__' -type d -exec rm -rf {} +
