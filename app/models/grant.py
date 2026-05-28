from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Grant(Base):
    __tablename__ = "grants"
    __table_args__ = {"schema": "grants_svc"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    document_id = Column(
        UUID(as_uuid=True),
        nullable=False,
    )

    grantee_id = Column(
        UUID(as_uuid=True),
        nullable=False,
    )

    created_by = Column(
        UUID(as_uuid=True),
        nullable=False,
    )

    permission = Column(String, nullable=False)

    expires_at = Column(DateTime(timezone=True), nullable=False)

    revoked_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )