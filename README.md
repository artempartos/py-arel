# Py-Arel

Python port of Arel library (Ruby) for building SQL queries via AST.

## Quick Start with Docker

### Requirements
- Docker
- Docker Compose (optional, can use `docker` directly)

### First Setup

```bash
# Quick check that everything works
./check-docker.sh

# Or manually:
docker-compose build
```

### Running Tests

```bash
# Build image (if not built yet)
make build
# or
docker-compose build

# Run all tests
make test
# or
docker-compose run --rm py-arel pytest tests/python -v

# Run specific test
make test-file FILE=test_table.py
# or
docker-compose run --rm py-arel pytest tests/python/test_table.py -v

# Run with coverage
docker-compose run --rm py-arel pytest tests/python --cov=arel --cov-report=html
```

### Interactive Work

```bash
# Start container in background
make up

# Enter container
make shell
# or
docker-compose exec py-arel /bin/bash

# Inside container you can run tests directly
pytest tests/python -v
python3 tests/python/test_table.py
```

### Cleanup

```bash
# Stop and remove containers
make down

# Full cleanup (containers + images)
make clean
```

## Development without Docker

```bash
# Install dependencies
pip install -r requirements.txt

# Set PYTHONPATH
export PYTHONPATH=$PYTHONPATH:.

# Run tests
pytest tests/python -v
# or
python3 tests/python/test_table.py
```

## Project Structure

```
py-arel/
├── arel/              # Main library code
│   ├── nodes/        # AST nodes
│   ├── visitors/      # Visitors (SQL generation)
│   ├── collectors/   # SQL collectors
│   ├── mixins/       # Mixins (Predications, Math, etc.)
│   └── attributes/   # Table attributes
├── tests/python/     # Tests (pytest)
├── Dockerfile        # Docker image
├── docker-compose.yml # Docker Compose configuration
├── requirements.txt   # Python dependencies
└── Makefile          # Convenient commands
```

## Porting Status

Detailed porting status of all classes and tests see in [ai/09_test_coverage.md](ai/09_test_coverage.md)
