from datetime import date
from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    monthly_income: float
    savings_goal: float
    current_savings: float


class StudentOut(StudentCreate):
    id: int

    class Config:
        from_attributes = True


class TransactionCreate(BaseModel):
    student_id: int
    date: date
    category: str
    description: str
    amount: float


class TransactionOut(TransactionCreate):
    id: int

    class Config:
        from_attributes = True


class BudgetCreate(BaseModel):
    student_id: int
    category: str
    monthly_limit: float


class BudgetOut(BudgetCreate):
    id: int

    class Config:
        from_attributes = True
