from sqlalchemy import Column, Integer, String, DateTime, func
from app.config.database import Base

class RevokedToken(Base):
    __tablename__ = 'revoked_tokens'
    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String(255), unique=True, nullable=False)  # JWT ID
    token = Column(String(512), nullable=False)
    user_id = Column(Integer, nullable=False)
    revoked_at = Column(DateTime, nullable=False, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)
    reason = Column(String(255), nullable=True)
