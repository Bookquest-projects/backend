# backend

## Project setup

> [!WARNING]
> This project requires Python 3.10.0 or higher.

> ![WARNING]
> This project requires Docker if you want to run the database locally.

## Environment variables

Create a .env file in the root of the project with the following content:

```bash
SECRET_KEY="your_secret_key"

JWT_SECRET_KEY="your_jwt_secret"

DB_USER="sa"
DB_NAME="master"
SQLSERVER_PASS="abcDEF123#"
DB_HOST="localhost"
DEBUG="True"

ORIGIN="http://localhost:8080"
```

You can generate a secret key or a jwt secret key by running with Python:

```bash
python -c 'import os; print(os.urandom(16))'
```

Then copy the output and paste it in the .env file.

## Database setup

To set up the database, run:

go to the database folder:

```bash
cd database
```

```bash
docker build -t database .
```

Then run the database container:

```bash
docker run -d -p 5432:5432 database
```

## Backend setup

Return to the root of the project:

```bash
cd ..
```

Check your Python version:

```bash
python --version
```

If you have Python 3.10.0 or higher, you can continue with the setup,
otherwise, you need to install the correct version.

To setup a virtual environment, run:

```bash
python -m venv venv
```

To install the dependencies, run:

```bash
pip install -r requirements.txt
```

## Running the project

To start the project, run:

```bash
python bookquest/app/__init__.py
```

## Linting

To check lint errors, run:

```bash
flake8 bookquest --format=pylint
```
