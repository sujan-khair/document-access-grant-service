from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.api.grants import router as grants_router
from app.core.database import engine, Base, AsyncSessionLocal
from app.models.grant import Grant
from app.models.user import User
from app.models.document import Document

app = FastAPI(title="Document Access Grant Service")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS grants_svc"))
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        users = [
            User(id=UUID("11111111-1111-1111-1111-111111111111"), name="Alice", email="alice@test.com"),
            User(id=UUID("22222222-2222-2222-2222-222222222222"), name="Bob", email="bob@test.com"),
            User(id=UUID("33333333-3333-3333-3333-333333333333"), name="Carol", email="carol@test.com"),
        ]

        documents = [
            Document(id=UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"), title="Q1 Report"),
            Document(id=UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"), title="Product Roadmap"),
            Document(id=UUID("cccccccc-cccc-cccc-cccc-cccccccccccc"), title="Budget 2026"),
        ]

        for user in users:
            existing = await session.get(User, user.id)
            if not existing:
                session.add(user)

        for document in documents:
            existing = await session.get(Document, document.id)
            if not existing:
                session.add(document)

        await session.commit()

app.include_router(grants_router)
