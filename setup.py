from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(here, "HISTORY.md"), encoding="utf-8") as f:
    history = f.read()

setup(
    name="python-aws-dataclasses",
    version="0.4.0",
    packages=find_packages(exclude=["tests"]),
    install_requires=["dataclasses>=0.6; python_version == '3.6'", "arrow>=0.11.0"],
    package_data={"": ["*.txt", "*.rst", "*.md"]},
    author="Benjamin Weigel",
    author_email="benjamin.weigel@europace.de",
    description="Data classes for AWS stuff (lambda events etc.)",
    long_description=long_description + "\n\n" + history,
    license="Apache 2.0",
    keywords="aws lambda events",
    url="http://github.com/hypoport/python-aws-dataclasses",  # project home page, if any
    project_urls={
        "Bug Tracker": "http://github.com/hypoport/python-aws-dataclasses",
        "Documentation": "http://github.com/hypoport/python-aws-dataclasses",
        "Source Code": "http://github.com/hypoport/python-aws-dataclasses",
    },
    test_suite="tests",
)
