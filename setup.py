import os

from setuptools import setup, find_packages

readme = open('README.md').read()

tests_require = [
    'coverage>=4.5',
    'coveralls>=1.8',
    'pytest>=5.2',
    'pytest-cov>=2.8',
    'pytest-pep8>=1.0',
    'pydocstyle>=4.0',
]

extras_require = {
    'tests': tests_require,
}

extras_require['all'] = [req for exts, reqs in extras_require.items()
                         for req in reqs]

setup_requires = [
    'pytest-runner>=5.2',
]

with open(os.path.join('quart_rapidoc', 'version.py'), 'rt') as fp:
    g = {}
    exec(fp.read(), g)
    version = g['__version__']

with open('README.md') as f:
    long_description = f.read()

setup(
    name='Quart-Rapidoc',
    version=version,
    url='https://github.com/marirs/quart-rapidoc',
    license='MIT',
    author='Sriram G',
    author_email='marirs@gmail.com',
    description="Rapidoc support for openapi sepc",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require=extras_require,
    setup_requires=setup_requires,
    tests_require=tests_require,
    install_requires=[
        'Quart>=0.12.0',
        'PyYAML>=5.3'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: 3.8",
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.7',
)