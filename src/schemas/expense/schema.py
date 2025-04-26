from pydantic import BaseModel, Field
from typing import Optional
from datetime import date as Date


class ExpenseBase(BaseModel):
    title: str = Field(..., description="Name of the expense")


class ExpenseCreate(ExpenseBase):
    amount: float = Field(..., description="Amount of the expense")
    date: Date = Field(..., description="Date of the expense")


class ExpenseUpdate(ExpenseBase):
    title: Optional[str] = Field(None, description="Name of the expense")
    amount: Optional[float] = Field(None, description="Amount of the expense")
    date: Optional[Date] = Field(None, description="Date of the expense")


class ExpenseResponse(ExpenseBase):
    id: int = Field(..., description="ID of the expense")
    date: Date = Field(..., description="Date of the expense")
    amount: float = Field(..., description="Amount of the expense")
    usd_amount: float = Field(..., description="Amount of the expense in USD")

    class Config:
        from_attributes = True
