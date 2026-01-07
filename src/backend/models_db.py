from sqlalchemy import Column, Integer, String, Numeric, JSON, TIMESTAMP, func, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(128), unique=True, nullable=True)
    name = Column(String(256), nullable=True)
    email = Column(String(256), nullable=True)
    age = Column(Integer, nullable=True)
    income = Column(Numeric, nullable=True)
    state = Column(String(128), nullable=True)
    district = Column(String(128), nullable=True)
    needs = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Scheme(Base):
    __tablename__ = "schemes"
    id = Column(Integer, primary_key=True, index=True)
    scheme_id = Column(String(64), unique=True, nullable=False)
    title = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    metadata_json = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=True)
    benefits = Column(JSON, nullable=True)
    documents = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
