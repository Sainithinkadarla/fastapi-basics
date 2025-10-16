from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
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
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(1024), nullable=False)

class AccessToken(Base):
    __tablename__ = "access_tokens"
    token: Mapped[str] = mapped_column(String(1024), primary_key=True, default=generate_token)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    expiration_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=get_expiration_date)
    user: Mapped[User] = relationship('User', lazy="joined")

    def max_age(self):
        delta = self.expiration_date - datetime.now(tz= timezone.utc)
        return int(delta.total_seconds())