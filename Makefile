install:
	pip install -U pip
	pip install -e .[tests,docs]

tests:
	pydocstyle quart_rapidoc
	pytest
