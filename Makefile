lint:
	isort -rc .

tests:
	flake8
	mypy --no-strict-optional rules/
	pytest --cov-report term-missing --cov-branch --cov=rules tests/

.PHONY: lint tests
