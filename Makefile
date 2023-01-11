POETRY := poetry

.PHONY: default format test pytest doc

default: format doc

doc:
	@printf "pdoc:\n"
	@PYTHONWARNINGS=ignore ${POETRY} run pdoc dash_cytoscape_elements/ --html -o ./docs --force
	@mv ./docs/dash_cytoscape_elements/* ./docs/
	@rm -r ./docs/dash_cytoscape_elements/

format:
	@printf "black:\n"
	@${POETRY} run black .
	@printf "isort:\n"
	@${POETRY} run isort .

test:
	@printf "tox:\n"
	@${POETRY} run tox

pytest:
	@printf "pytest:\n"
	@${POETRY} run pytest ./tests -v
