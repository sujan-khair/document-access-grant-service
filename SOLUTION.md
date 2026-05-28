Implemented async FastAPI REST API with PostgreSQL and SQLAlchemy 2.0.
Added required business rules and grant validation.
Implemented grants_svc schema with users, documents, and grants tables.
Added deterministic UUID seed data for users and documents.
Included Alembic migration with upgrade() and downgrade() support.
Added Docker Compose setup for PostgreSQL and API service.
Added unit and integration-style API tests using pytest.
Used Pydantic v2 schemas and async database sessions.
Inactive grants remain permanently stored.
Swagger docs available at /docs.
