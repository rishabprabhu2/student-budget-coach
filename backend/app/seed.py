from datetime import date
import random

from .database import Base, engine, SessionLocal
from .models import Student, Transaction, Budget

random.seed(42)

categories = ["Food", "Rent", "Transportation", "Entertainment", "Books", "Subscriptions", "Savings", "Shopping"]

student_names = [
    "Alex Johnson", "Maya Patel", "Jordan Lee", "Sofia Garcia", "Ethan Brown", "Ava Wilson", "Noah Kim",
    "Olivia Chen", "Liam Davis", "Emma Martinez", "Lucas Smith", "Isabella Nguyen", "Mason Clark", "Mia Robinson"
]

budget_ranges = {
    "Food": (250, 450),
    "Rent": (700, 1200),
    "Transportation": (60, 180),
    "Entertainment": (80, 220),
    "Books": (40, 160),
    "Subscriptions": (20, 80),
    "Savings": (100, 450),
    "Shopping": (80, 250)
}

transaction_descriptions = {
    "Food": ["Groceries", "Coffee", "Dining hall", "Takeout", "Restaurant"],
    "Rent": ["Monthly rent"],
    "Transportation": ["Bus pass", "Gas", "Uber", "Train ticket"],
    "Entertainment": ["Movie", "Concert", "Game night", "Streaming"],
    "Books": ["Textbook", "Course packet", "Notebook", "Online course"],
    "Subscriptions": ["Spotify", "Cloud storage", "Gym", "Streaming"],
    "Savings": ["Savings transfer"],
    "Shopping": ["Clothes", "Dorm supplies", "Electronics", "Personal care"]
}


def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    for name in student_names:
        student = Student(
            name=name,
            monthly_income=random.randint(1400, 3200),
            savings_goal=random.randint(1000, 5000),
            current_savings=random.randint(150, 2500)
        )
        db.add(student)
        db.flush()

        for category in categories:
            low, high = budget_ranges[category]
            db.add(Budget(
                student_id=student.id,
                category=category,
                monthly_limit=random.randint(low, high)
            ))

        for month in range(1, 6):
            for _ in range(random.randint(16, 24)):
                category = random.choice(categories)
                if category == "Rent":
                    amount = random.randint(700, 1200)
                elif category == "Savings":
                    amount = random.randint(50, 250)
                else:
                    amount = round(random.uniform(6, 95), 2)

                db.add(Transaction(
                    student_id=student.id,
                    date=date(2026, month, random.randint(1, 28)),
                    category=category,
                    description=random.choice(transaction_descriptions[category]),
                    amount=amount
                ))

    db.commit()
    db.close()
    print("Seeded database with 14 students, budgets, and transactions.")


if __name__ == "__main__":
    seed()
