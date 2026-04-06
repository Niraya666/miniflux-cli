.PHONY: install install-dev fmt lint test docker-up docker-down e2e clean

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

fmt:
	ruff format src tests

lint:
	ruff check src tests
	mypy src

test:
	pytest tests/

docker-up:
	docker compose -f docker/docker-compose.yaml up -d

docker-down:
	docker compose -f docker/docker-compose.yaml down -v

e2e: install-dev docker-up
	@echo "Waiting for Miniflux to be ready..."
	@for i in 1 2 3 4 5 6 7 8 9 10; do \
		if curl -sf http://localhost/healthcheck >/dev/null 2>&1; then break; fi; \
		echo "... ($$i/10)"; sleep 3; \
	done
	bash scripts/e2e.sh

clean:
	rm -rf build/ dist/ .pytest_cache/ .coverage/ htmlcov/ src/*.egg-info
