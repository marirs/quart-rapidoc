import pytest
from .quart_rapidoc_tests.test_quart_rapidoc import TestQuartRapidoc

if __name__ == '__main__':
    pytest.main(['--color=auto', '--no-cov', '-v'])
