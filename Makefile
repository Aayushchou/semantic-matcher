test:
	python3 -m pytest tests/

install: 
	python3 -m pip install . 

install-dev: 
	python3 -m pip install -e .[dev]

precommit: 
	python3 -m black .

