from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime, timedelta, timezone
import secrets

def get_expiration_date(seconds: int = 86400):
    return datetime.now(tz=timezone.utc) + timedelta(seconds=seconds)

def generate_token():
    return secrets.token_urlsafe(32)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    email: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
    passwd: Mapped[str] = mapped_column(String(1024), nullable=False)

class AccessToken(Base):
    __tablename__ = "access_tokens"
    token: Mapped[str] = mapped_column(String(1024), primary_key=True, default=generate_token)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    expiration_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=get_expiration_date)

    user: Mapped[User] = relationship("User", lazy="joined")