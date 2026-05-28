from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta, UTC

from app.core.database import get_db
from app.models.grant import Grant
from app.schemas.grant import GrantCreate

router = APIRouter(prefix="/grants", tags=["Grants"])


@router.post("")
async def create_grant(payload: GrantCreate, db: AsyncSession = Depends(get_db)):
    if payload.expires_at <= datetime.now(UTC) + timedelta(minutes=1):
        raise HTTPException(status_code=400, detail="Expiry must be at least 1 minute ahead")

    existing = await db.scalar(select(Grant).where(Grant.document_id == payload.document_id, Grant.grantee_id == payload.grantee_id, Grant.revoked_at.is_(None)))

    if existing:
        raise HTTPException(status_code=409, detail="Active grant already exists")

    grant = Grant(**payload.model_dump())
    db.add(grant)
    await db.commit()
    await db.refresh(grant)
    return grant


@router.get("")
async def list_grants(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Grant))
    return result.scalars().all()


@router.get("/{grant_id}")
async def get_grant(grant_id, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Grant).where(Grant.id == grant_id))
    grant = result.scalar_one_or_none()

    if not grant:
        raise HTTPException(404, "Grant not found")

    return grant


@router.get("/{grant_id}/check")
async def check_grant(grant_id, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Grant).where(Grant.id == grant_id))
    grant = result.scalar_one_or_none()

    if not grant:
        raise HTTPException(404, "Grant not found")

    active = grant.revoked_at is None and grant.expires_at > datetime.now(UTC)
    return {"active": active}


@router.delete("/{grant_id}")
async def revoke_grant(grant_id, creator_id, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Grant).where(Grant.id == grant_id))
    grant = result.scalar_one_or_none()

    if not grant:
        raise HTTPException(404, "Grant not found")

    if str(grant.created_by) != str(creator_id):
        raise HTTPException(403, "Only creator can revoke")

    if grant.revoked_at is not None:
        raise HTTPException(400, "Grant already revoked")

    if grant.expires_at <= datetime.now(UTC):
        raise HTTPException(400, "Grant already expired")

    grant.revoked_at = datetime.now(UTC)
    await db.commit()

    return {"message": "Grant revoked"}
