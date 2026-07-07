from sqlalchemy.orm import Session
from . import models, schemas


def get_students(db: Session):
    return db.query(models.Student).order_by(models.Student.id).all()


def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def create_student(db: Session, student: schemas.StudentCreate):
    row = models.Student(**student.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_transactions(db: Session, student_id: int | None = None):
    query = db.query(models.Transaction)
    if student_id:
        query = query.filter(models.Transaction.student_id == student_id)
    return query.order_by(models.Transaction.date.desc()).all()


def create_transaction(db: Session, tx: schemas.TransactionCreate):
    row = models.Transaction(**tx.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_budgets(db: Session, student_id: int):
    return db.query(models.Budget).filter(models.Budget.student_id == student_id).all()


def create_budget(db: Session, budget: schemas.BudgetCreate):
    row = models.Budget(**budget.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
