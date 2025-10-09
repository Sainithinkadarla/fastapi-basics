from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, autoincrement = True, primary_key = True)
    publication_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    title : Mapped[str] = mapped_column(String(355), nullable=False)
    content : Mapped[str] = mapped_column(Text, nullable=False)