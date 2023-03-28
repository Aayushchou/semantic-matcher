test:
	python3 -m pytest tests/

install: 
	python3 -m pip install . 

install-dev:
	python3 -m pip install -e .
	python3 -m pip install -e .[dev]
	python3 -m pip install -e .[test]

precommit: 
	python3 -m black .

