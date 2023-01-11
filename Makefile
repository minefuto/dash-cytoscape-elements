POETRY := poetry

.PHONY: format test

format:
	@printf "black:\n"
	@${POETRY} run black .
	@printf "\n"
	@printf "isort:\n"
	@${POETRY} run isort .

test:
	@${POETRY} run tox

pytest:
	@${POETRY} run pytest ./tests -v
