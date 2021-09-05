# Zephyr

(WIP) Social Music Application built with FastAPI.

## Focus on Implementation

- Well-structured Project
- High Performance: Caching & Asynchronous I/O
- TDD: Test Driven Development
- Dockerized Environment
- CI/CD: Process Automation

## Requirements

- Python 3.8+
- Docker
- Docker Compose
- Poetry

<hr>

## Boilerplate

If you need boilerplate settings to launch your project, clone v1.0.0.

```shell
git clone https://github.com/qu3vipon/zephyr-backend.git
git checkout tags/v1.0.0 -b <branch_name>
```

<hr>

## Local Development

### Environment Variables

```shell
export SECRET_KEY
export ENV=dev
export TESTING=0
export DB_SERVER
export DB_USER
export DB_PASSWORD
export DB_NAME
```

### Run Server

```shell
docker-compose -f docker-compose-dev.yml up -d --build
```

### Run Test

```shell
docker-compose -f docker-compose-test.yml up --build --exit-code-from test_app
```

<hr>

## Database Migrations

### Update new models

When you create a new model, upload two files below to use it in your project.

```python
# zephyr/app/models/__init__.py 
#  -> to shorten import path
# zephyr/app/models/__all_models.py 
#  -> used by Alembic to generate revision script
```

### Populate migration script by Alembic

```shell
alembic revision --autogenerate -m "<revision message>"
```

### Run migration to head

```shell
alembic upgrade head
```
