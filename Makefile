install:
	pip install -U pip
	pip install -e .[tests,docs]

tests:
	pydocstyle quart_rapidoc
	isort --check-only --diff --recursive flask_redoc/*.pydocstyle
	pytest
