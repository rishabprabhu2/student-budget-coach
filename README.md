# Student Budget Coach

A full-stack finance platform for students to track spending, manage budgets, and visualize savings progress.

**Stack:** Python, FastAPI, React, PostgreSQL

## Features

- Add and view student spending transactions
- Track category budgets
- View savings progress
- Interactive dashboard with 15+ financial metrics
- PostgreSQL database with seed data for 14 students
- REST API backend
- React frontend dashboard

## Project Structure

```text
student-budget-coach/
  backend/
    app/
      main.py
      database.py
      models.py
      schemas.py
      seed.py
      analytics.py
      crud.py
    requirements.txt
    .env.example
  frontend/
    index.html
    package.json
    src/
      main.jsx
      App.jsx
      api.js
      styles.css
```

## Backend Setup

```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

Update `.env` if needed:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/student_budget_coach
```

Create the PostgreSQL database:

```bash
createdb student_budget_coach
```

Seed the database:

```bash
python -m app.seed
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

## Resume Description

**Student Budget Coach | Python, React, PostgreSQL**  
- Developed a finance platform that helped 14 students track spending, manage budgets, and visualize savings progress  
- Created interactive dashboards displaying 15+ financial metrics, including spending trends and budget utilization
