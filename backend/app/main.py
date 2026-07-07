from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import crud, schemas, analytics

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Budget Coach API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Student Budget Coach API"}


@app.get("/students", response_model=list[schemas.StudentOut])
def list_students(db: Session = Depends(get_db)):
    return crud.get_students(db)


@app.post("/students", response_model=schemas.StudentOut)
def add_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)


@app.get("/transactions", response_model=list[schemas.TransactionOut])
def list_transactions(student_id: int | None = None, db: Session = Depends(get_db)):
    return crud.get_transactions(db, student_id)


@app.post("/transactions", response_model=schemas.TransactionOut)
def add_transaction(tx: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db, tx)


@app.get("/budgets/{student_id}", response_model=list[schemas.BudgetOut])
def list_budgets(student_id: int, db: Session = Depends(get_db)):
    return crud.get_budgets(db, student_id)


@app.post("/budgets", response_model=schemas.BudgetOut)
def add_budget(budget: schemas.BudgetCreate, db: Session = Depends(get_db)):
    return crud.create_budget(db, budget)


@app.get("/analytics/student/{student_id}")
def student_dashboard(student_id: int, db: Session = Depends(get_db)):
    data = analytics.get_dashboard_metrics(db, student_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return data


@app.get("/analytics/platform")
def platform_dashboard(db: Session = Depends(get_db)):
    return analytics.get_platform_metrics(db)
