# Document Access Grant Service

A REST API built with FastAPI for managing document access grants between users.

## Features

* Create document access grants
* Revoke grants
* Check active/inactive grants
* Expiration validation
* Duplicate active grant prevention
* PostgreSQL + SQLAlchemy Async
* Dockerized setup
* Alembic migrations
* Unit and integration tests

---

## Tech Stack

* Python 3.11+
* FastAPI
* SQLAlchemy 2.0 (Async)
* PostgreSQL
* asyncpg
* Alembic
* Pydantic v2
* pytest + pytest-asyncio
* Docker

---

## Run Project

```bash
docker compose up --build
```

Application:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

## API Endpoints

| Method | Endpoint                 | Description        |
| ------ | ------------------------ | ------------------ |
| POST   | /grants                  | Create a grant     |
| GET    | /grants                  | List grants        |
| GET    | /grants/{grant_id}       | Get single grant   |
| DELETE | /grants/{grant_id}       | Revoke grant       |
| GET    | /grants/{grant_id}/check | Check grant status |

---

## Business Rules

1. Expiry must be at least 1 minute in the future
2. Only one active grant per grantee/document pair
3. Only creator can revoke grant
4. Cannot revoke expired or revoked grants
5. Inactive grants remain stored permanently

---

## Run Tests

```bash
pytest
```

---

## Seed Data

### Users

* Alice
* Bob
* Carol

### Documents

* Q1 Report
* Product Roadmap
* Budget 2026
