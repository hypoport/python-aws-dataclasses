Python-AWS-Dataclasses [WIP]
===========
[![Codecov](https://img.shields.io/codecov/c/github/hypoport/python-aws-dataclasses.svg)](https://github.com/hypoport/python-aws-dataclasses) ![GitHub](https://img.shields.io/github/license/hypoport/python-aws-dataclasses.svg) [![PyPI](https://img.shields.io/pypi/v/python-aws-dataclasses.svg)](https://pypi.org/project/python-aws-dataclasses/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-aws-dataclasses.svg)](https://pypi.org/project/python-aws-dataclasses/)

Python-AWS-Dataclasses provides data-classes for AWS lambda events and other AWS data.
The dataclasses are type-annotated, as to allow for full IDE (code completion / IntelliSense) support.

## Quickstart

### Installation

```bash
# using pip
pip install python-aws-dataclasses
# or using pipenv
pipenv install python-aws-dataclasses.git
```

### Usage 

Assuming you have a dict of some AWS event (e.g. events passed into your `lambda_handler`) use the `from_event()`-method and access the objects via the _dot_-notation.

```python
def lambda_handler(event, context):
  # Example 1: Lambda asynchronously invoked via SNS
  sns_event = SnsEvent.from_event(event)
  print(sns_event.first_record.sns.message)

  # Example 2: Lambda asynchronously invoked via S3-Event
  s3_event = S3Event.from_event(event)
  print(s3_event.first_record.s3.bucket.name)
```

## Contribution

Everyone is free to contribute and submit Pull-Requests.

## Misc

**Test using tox**

```
tox
```

**Test using setup.py**

```
python setup.py test
```
