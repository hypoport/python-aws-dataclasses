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
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="python-aws-dataclasses",
    version="0.1.0",
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
    description="Data classes for AWS stuff (lambda events etc.)",
    long_description=long_description,
    license="Apache 2.0",
    keywords="aws lambda events",
    url="http://github.com/hypoport/python-aws-dataclasses",  # project home page, if any
    project_urls={
        "Bug Tracker": "http://github.com/hypoport/python-aws-dataclasses",
        "Documentation": "http://github.com/hypoport/python-aws-dataclasses",
        "Source Code": "http://github.com/hypoport/python-aws-dataclasses",
    },

    test_suite="aws_dataclasses.test"

)
