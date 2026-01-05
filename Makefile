.PHONY: build up down test shell clean

# Build image
build:
	docker-compose build

# Start container
up:
	docker-compose up -d

# Stop container
down:
	docker-compose down

# Run all tests
test:
	docker-compose run --rm py-arel pytest tests/python -v

# Run specific test
test-file:
	docker-compose run --rm py-arel pytest tests/python/$(FILE) -v

# Interactive shell in container
shell:
	docker-compose run --rm py-arel /bin/bash

# Clean images and containers
clean:
	docker-compose down -v
	docker rmi py-arel-py-arel 2>/dev/null || true

# Rebuild image
rebuild:
	docker-compose build --no-cache

# View logs
logs:
	docker-compose logs -f py-arel

