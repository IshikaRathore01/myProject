# Python ORM for PostgreSQL

This project is a Python script that serves as an Object-Relational Mapping (ORM) for PostgreSQL. It allows you to interact with a PostgreSQL database using Python objects and provides functionality to perform common database operations.

## Prerequisites

- Python 3
- PostgreSQL

## Libraries Used

- Alembic
- SQLAlchemy
- Psycopg2

## Installation

To install the required external modules, run:

```
pip install alembic
pip install sqlalchemy psycopg2-binary
```

## Database Configuration

Before running the script, you need to set up a PostgreSQL database. Follow these steps:

1. Install PostgreSQL if you haven't already.
2. Create a new PostgreSQL database and user. You can use the following SQL commands as an example:

```sql
CREATE DATABASE testdb;
CREATE USER postgres WITH PASSWORD '1234';
```

3. Update the database configuration in `server.py`. You'll need to provide the database name, username, password, and host. Here's an example:

```python
# Database configuration
DATABASE_NAME = 'testdb'
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = '1234'
DATABASE_HOST = 'localhost'  # or your PostgreSQL host address
DATABASE_PORT = '5432'  # or your PostgreSQL port
```

## How to Run the Script

Execute the following command:

```
python server.py
```

The server will run on port 8000 by default.
