from typing import Optional
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///db1.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": True})

Base = declarative_base()
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db1 = SessionLocal()


class TaskBase(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, nullable=False)
    title = Column(String(80), nullable=False)
    description = Column(String(80), nullable=False)
    status = Column(String(80), nullable=False)
    is_del = Column(Boolean, nullable=False)


class Task(BaseModel):
    task_id: int
    title: Optional[str] = None
    description: str
    status: Optional[str] = None


class MoviesBase(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, nullable=False)
    title = Column(String(80), nullable=False)
    description = Column(String(80), nullable=False)
    genre = Column(String(80), nullable=False)
    is_del = Column(Boolean, nullable=False)


class Movies(BaseModel):
    movie_id: int
    title: Optional[str] = None
    description: str
    genre: Optional[str] = None


class UsersBase(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    password = Column(String(80), nullable=False)
    is_del = Column(Boolean, nullable=False)


class Users(BaseModel):
    user_id: int
    name: Optional[str] = None
    email: str
    password: Optional[str] = None

