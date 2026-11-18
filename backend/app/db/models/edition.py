from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Edition(Base):
    __tablename__ = "editions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="DRAFT",
        nullable=False,
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    articles = relationship(
        "EditionArticle",
        back_populates="edition",
        cascade="all, delete-orphan",
    )


class EditionArticle(Base):
    __tablename__ = "edition_articles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    edition_id: Mapped[int] = mapped_column(
        ForeignKey("editions.id"),
        nullable=False,
    )

    article_id: Mapped[int] = mapped_column(
        ForeignKey("articles.id"),
        nullable=False,
    )

    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    edition = relationship(
        "Edition",
        back_populates="articles",
    )

    article = relationship(
        "Article",
    )