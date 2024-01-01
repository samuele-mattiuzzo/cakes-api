# Cakes API

A simple Django project that features a Cakes api

- Runs on Docker
- Provides a Swagger documentation
- Provides a [Postman](https://www.postman.com/) collection

## Pre-requisites

- [Python](https://www.python.org/) >= 3.11
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## Setup

- Clone the project

- Cd into the project's directory

- Copy the file `.env.dist` to a new file called `.env`

  - the provided variables are enough to start with


### Docker setup

- Ensure Docker is up and running

- Run the containers

```bash
$> docker compose up
```

- To seed some data, run

```bash
$> docker exec -it <container name> python manage.py test_seed
```

### Native setup

- Create a virtualenv

```bash
$> python -m venv .venv
```

- Activate the virtual environment

```bash
$> source .venv/bin/activate
```

- Install the required dependencies

```bash
$> python -m pip install -r requirements.txt
```

- Open the `.env` file and change the value of `USE_SQLITE` from 0 to 1

- Run the migrations

```bash
$> python manage.py migrate
```

- Seed some data (use the `--wipe` option to wipe any existing database)

```bash
$> python manage.py test_seed [--wipe]
```

---

## Running tests

### Using Docker

```bash
$> docker exec -it <container name> python manage.py test
```

### Natively

```bash
$> python manage.py test
```

---

## Documentation

The documentation is available at `http://localhost:8000/documentation/` in OpenAPI format using ReDoc

## Production

The app also comes supplied with Nginx and a second docker-compose file to use within a production environment.
It will start a Gunicorn app

```bash
$> docker compose -f docker-compose-prod.yml up
```
