"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="LaWip",
    version="0.0.1",
    packages=find_packages(exclude=["*.test"]),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['docutils>=0.3'],

    package_data={
        '': ['*.txt', '*.rst', '*.md']
    },

    # metadata for upload to PyPI
    author="Benjamin Weigel",
    author_email="benjamin.weigel@europace.de",
    description="Data classes for AWS lambda events",
    long_description=long_description,
    license="Apache 2.0",
    keywords="aws lambda events",
    url="http://github.com/bweigel/lawip",  # project home page, if any
    project_urls={
        "Bug Tracker": "http://github.com/bweigel/lawip",
        "Documentation": "http://github.com/bweigel/lawip",
        "Source Code": "http://github.com/bweigel/lawip",
    },

    test_suite="lawip.test.test_s3_event"

)
