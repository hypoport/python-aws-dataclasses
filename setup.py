from setuptools import setup, find_packages

setup(
    name="python-aws-dataclasses",
    version="0.4.3",
    packages=find_packages(exclude=["tests"]),

    install_requires=['docutils>=0.3',
                      'dataclasses>=0.6',
                      'arrow>=0.11.0'],

    package_data={
        '': ['*.txt', '*.rst', '*.md']
    },
    test_suite="tests"
)
