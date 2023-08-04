coverage:  ## Run tests with coverage
	ENDPOINT_EXTRA_SOURCE_SERVICE=http://test poetry run pytest --cov --cov-report html -vv .

deps:  ## Install dependencies
	poetry install --no-root && 

lint:
	poetry run black app
	poetry run isort app
	
ruff:
	poetry run ruff app

fix-ruff:
	poetry run ruff --fix app

mypy:
	poetry run mypy app

test:  ## Run tests
	ENDPOINT_EXTRA_SOURCE_SERVICE=http://test poetry run pytest -vv .

run:  ## Run project
	docker compose up

build:  ## build images
	docker compose build --no-cache

