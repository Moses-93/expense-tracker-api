from pydantic import BaseModel, Field
from typing import Optional
from datetime import date as Date


class ExpenseBase(BaseModel):
    name: str = Field(..., description="Name of the expense")


class ExpenseCreate(ExpenseBase):
    uah_amount: float = Field(..., description="Amount of the expense")
    date: Date = Field(..., description="Date of the expense")


class ExpenseUpdate(ExpenseBase):
    name: Optional[str] = Field(None, description="Name of the expense")
    uah_amount: Optional[float] = Field(None, description="Amount of the expense")
    date: Optional[Date] = Field(None, description="Date of the expense")


class ExpenseResponse(ExpenseBase):
    id: int = Field(..., description="ID of the expense")
    date: Date = Field(..., description="Date of the expense")
    uah_amount: float = Field(..., description="Amount of the expense")
    usd_amount: float = Field(..., description="Amount of the expense in USD")

    class Config:
        from_attributes = True
