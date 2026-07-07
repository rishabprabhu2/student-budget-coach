from collections import defaultdict
from sqlalchemy.orm import Session
from .models import Student, Transaction, Budget


def get_dashboard_metrics(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return None

    transactions = db.query(Transaction).filter(Transaction.student_id == student_id).all()
    budgets = db.query(Budget).filter(Budget.student_id == student_id).all()

    total_spending = sum(t.amount for t in transactions)
    transaction_count = len(transactions)
    avg_transaction = total_spending / transaction_count if transaction_count else 0

    spending_by_category = defaultdict(float)
    spending_by_month = defaultdict(float)

    for t in transactions:
        spending_by_category[t.category] += t.amount
        spending_by_month[t.date.strftime("%Y-%m")] += t.amount

    budget_total = sum(b.monthly_limit for b in budgets)
    budget_used_pct = (total_spending / budget_total * 100) if budget_total else 0

    highest_category = max(spending_by_category, key=spending_by_category.get) if spending_by_category else "N/A"
    highest_category_amount = spending_by_category.get(highest_category, 0)

    savings_progress_pct = (student.current_savings / student.savings_goal * 100) if student.savings_goal else 0
    remaining_savings_needed = max(student.savings_goal - student.current_savings, 0)

    estimated_monthly_surplus = student.monthly_income - total_spending
    savings_rate_pct = (estimated_monthly_surplus / student.monthly_income * 100) if student.monthly_income else 0

    budget_utilization = []
    for b in budgets:
        spent = spending_by_category.get(b.category, 0)
        budget_utilization.append({
            "category": b.category,
            "budget": round(b.monthly_limit, 2),
            "spent": round(spent, 2),
            "utilization_pct": round((spent / b.monthly_limit * 100) if b.monthly_limit else 0, 1)
        })

    return {
        "student": {
            "id": student.id,
            "name": student.name,
            "monthly_income": student.monthly_income,
            "savings_goal": student.savings_goal,
            "current_savings": student.current_savings
        },
        "kpis": {
            "total_spending": round(total_spending, 2),
            "transaction_count": transaction_count,
            "average_transaction": round(avg_transaction, 2),
            "monthly_income": round(student.monthly_income, 2),
            "budget_total": round(budget_total, 2),
            "budget_used_pct": round(budget_used_pct, 1),
            "highest_spending_category": highest_category,
            "highest_category_amount": round(highest_category_amount, 2),
            "savings_goal": round(student.savings_goal, 2),
            "current_savings": round(student.current_savings, 2),
            "savings_progress_pct": round(savings_progress_pct, 1),
            "remaining_savings_needed": round(remaining_savings_needed, 2),
            "estimated_monthly_surplus": round(estimated_monthly_surplus, 2),
            "savings_rate_pct": round(savings_rate_pct, 1),
            "categories_tracked": len(spending_by_category),
            "budgets_created": len(budgets)
        },
        "spending_by_category": [
            {"category": k, "amount": round(v, 2)}
            for k, v in sorted(spending_by_category.items(), key=lambda x: x[1], reverse=True)
        ],
        "spending_by_month": [
            {"month": k, "amount": round(v, 2)}
            for k, v in sorted(spending_by_month.items())
        ],
        "budget_utilization": budget_utilization
    }


def get_platform_metrics(db: Session):
    students = db.query(Student).all()
    transactions = db.query(Transaction).all()

    total_users = len(students)
    total_transactions = len(transactions)
    total_spending = sum(t.amount for t in transactions)

    avg_spending_per_student = total_spending / total_users if total_users else 0
    avg_savings_progress = (
        sum((s.current_savings / s.savings_goal * 100) for s in students if s.savings_goal) / total_users
        if total_users else 0
    )

    category_totals = defaultdict(float)
    for t in transactions:
        category_totals[t.category] += t.amount

    return {
        "total_students": total_users,
        "total_transactions": total_transactions,
        "total_platform_spending": round(total_spending, 2),
        "average_spending_per_student": round(avg_spending_per_student, 2),
        "average_savings_progress_pct": round(avg_savings_progress, 1),
        "top_categories": [
            {"category": k, "amount": round(v, 2)}
            for k, v in sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        ]
    }
