from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    Date,
    Integer,
    Numeric,
    String,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=True)
    chat_id = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())

    # Relationships
    expenses = relationship("Expense", back_populates="user")


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(50), nullable=True)
    date = Column(Date, nullable=False)
    uah_amount = Column(Numeric(10, 2), nullable=False)
    usd_amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    # Relationships
    user = relationship("User", back_populates="expenses")
