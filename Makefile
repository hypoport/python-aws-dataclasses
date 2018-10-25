.PHONY: docs test clean clean-build clean-pyc clean-test publish

init:
	pip install pipenv --upgrade
	pipenv install --dev --skip-lock

test:
	pipenv run pytest -v

test-all:
	# This runs all of the tests, on both Python 2 and Python 3.
	detox

check:
	mypy -p aws_dataclasses

ci:
	pipenv run pytest --junitxml=report.xml

test-metadata:
	@pipenv run python setup.py check -mr --strict && \
	([ $$? -eq 0 ] && echo "Metadata ok.") || echo "Metdata might be missing or incorrect."

flake8:
	pipenv run flake8 --ignore=E501,F401,E128,E402,E731,F821 requests

coverage:
	pipenv run pytest --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=aws_dataclasses tests

publish:
	flit --repository testpypi publish

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . \( -path ./env -o -path ./venv -o -path ./.env -o -path ./.venv \) -prune -o -name '*.egg-info' -exec rm -fr {} +
	find . \( -path ./env -o -path ./venv -o -path ./.env -o -path ./.venv \) -prune -o -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -fr .cache