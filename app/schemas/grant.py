from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from enum import Enum


class PermissionEnum(str, Enum):
    view = "view"
    edit = "edit"
    admin = "admin"


class GrantCreate(BaseModel):
    document_id: UUID
    grantee_id: UUID
    created_by: UUID
    permission: PermissionEnum
    expires_at: datetime


class GrantResponse(GrantCreate):
    id: UUID
    revoked_at: datetime | None = None

    class Config:
        from_attributes = True