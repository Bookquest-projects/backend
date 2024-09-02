from lib2to3.pygram import python_symbolsfrom ctypes import pydll

# backend

## Project setup

> [!WARNING]
> This project requires Python 3.10.0 or higher.

To install the dependencies, run:

```bash
pip install -r requirements.txt
```

## Running the project

Create a secret key for the Flask app and a secret key for the JWT tokens.

```sh
python -c "import os; print(os.urandom(16).hex())"
```

Create a `.env` file in the root of the project and add the generated
secret key:

```bash
JWT_SECRET_KEY=<JWT_SECRET_KEY>
```

To start the project, run:

```bash
python bookquest/app/__init__.py
```

## Linting

To lint the project, run:

```bash
flake8 bookquest --format=pylint
```
