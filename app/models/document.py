from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base

class Document(Base):
    __tablename__="documents"
    __table_args__={"schema":"grants_svc"}
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title=Column(String, nullable=False)
