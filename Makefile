POETRY := poetry

.PHONY: default black doc isort mypy test pytest

default: black isort mypy pytest

black:
	@printf "black:\n"
	@${POETRY} run black .

doc:
	@printf "pdoc:\n"
	@PYTHONWARNINGS=ignore ${POETRY} run pdoc dash_cytoscape_elements/ --html -o ./docs --force
	@mv ./docs/dash_cytoscape_elements/* ./docs/
	@rm -r ./docs/dash_cytoscape_elements/

isort:
	@printf "isort:\n"
	@${POETRY} run isort .

mypy:
	@printf "mypy:\n"
	@${POETRY} run mypy .

test:
	@printf "tox:\n"
	@${POETRY} run tox

pytest:
	@printf "pytest:\n"
	@${POETRY} run pytest ./tests -v
