import enum

from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, Enum, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Role(enum.Enum):
    admin: str = 'admin'
    moderator: str = 'moderator'
    user: str = 'user'


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    phone_number = Column(String)
    birth_date = Column(Date)
    additional_data = Column(String, nullable=True)
    # updated: bool
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(150))
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(300), nullable=False)
    refresh_token = Column(String(300), nullable=True)
    avatar = Column(String(300), nullable=True)
    roles = Column('roles', Enum(Role), default=Role.user)
    confirmed = Column(Boolean, default=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
