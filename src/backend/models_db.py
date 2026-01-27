from sqlalchemy import Integer, String, Numeric, JSON, TIMESTAMP, func, Text
# Use new SQLAlchemy 2.x import path to avoid MovedIn20Warning
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from typing import Optional, Any

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    external_id: Mapped[Optional[str]] = mapped_column(String(128), unique=True, nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    income: Mapped[Optional[Any]] = mapped_column(Numeric, nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    district: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    needs: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[Any] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())


class Scheme(Base):
    __tablename__ = "schemes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    scheme_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    eligibility: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    application: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    level: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    scheme_category: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    metadata_json: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    tags: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    benefits: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    documents: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[Any] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
