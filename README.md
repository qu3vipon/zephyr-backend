# Zephyr
Social Music Application built with FastAPI

## Requirements
- Python 3.8+
- Docker
- Docker Compose
- Poetry

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