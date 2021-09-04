# Zephyr

Social Music Application built with FastAPI

## Requirements

- Python 3.8+
- Docker
- Docker Compose
- Poetry

<hr>

## Boilterplate

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

```python
# zephyr/app/models/__init__.py 
#  -> to shorten import path
# zephyr/app/models/__all_models.py 
#  -> used by Alembic to generate revision script
```

### Populate revision script by Alembic

```shell
alembic revision --autogenerate -m "revision message"
```
