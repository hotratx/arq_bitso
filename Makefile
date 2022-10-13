.PHONY: isort
isort:
	isort

.PHONY: black
black:
	black . *.py

.PHONY: clean
clean:
	find . -type f -name "*.pyc" | xargs rm -fr

	find . -type d -name __pycache__ | xargs rm -fr

.PHONY: checklist
checklist: isort black clean
