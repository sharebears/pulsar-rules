lint:
	isort -rc .
_tests:
	flake8
	mypy --no-strict-optional rules/
	pytest --cov-report term-missing --cov-branch --cov=rules tests/
tests: _tests
