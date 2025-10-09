from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, Relationship

class Base(DeclarativeBase):
    pass

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    publication_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    post: Mapped["Post"] = Relationship("Post", back_populates="comments")

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, autoincrement = True, primary_key = True)
    publication_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    title : Mapped[str] = mapped_column(String(355), nullable=False)
    content : Mapped[str] = mapped_column(Text, nullable=False)
    comments: Mapped[list[Comment]] = Relationship("Comment", cascade="all, delete")