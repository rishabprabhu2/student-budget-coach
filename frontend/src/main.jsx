import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, PieChart, Pie, Cell
} from "recharts";
import { getStudents, getStudentAnalytics, getPlatformAnalytics } from "./api";
import "./styles.css";

function KpiCard({ label, value }) {
  return (
    <div className="kpi-card">
      <p>{label}</p>
      <h3>{value}</h3>
    </div>
  );
}

function App() {
  const [students, setStudents] = useState([]);
  const [selectedStudentId, setSelectedStudentId] = useState(1);
  const [dashboard, setDashboard] = useState(null);
  const [platform, setPlatform] = useState(null);

  useEffect(() => {
    getStudents().then((data) => {
      setStudents(data);
      if (data.length > 0) setSelectedStudentId(data[0].id);
    });
    getPlatformAnalytics().then(setPlatform);
  }, []);

  useEffect(() => {
    if (selectedStudentId) {
      getStudentAnalytics(selectedStudentId).then(setDashboard);
    }
  }, [selectedStudentId]);

  if (!dashboard) {
    return <div className="page">Loading dashboard...</div>;
  }

  const k = dashboard.kpis;

  return (
    <div className="page">
      <header className="hero">
        <div>
          <p className="eyebrow">Python • React • PostgreSQL</p>
          <h1>Student Budget Coach</h1>
          <p>
            A student finance dashboard for tracking spending, managing budgets,
            and visualizing savings progress across real financial metrics.
          </p>
        </div>

        <div className="selector-card">
          <label>Choose student</label>
          <select
            value={selectedStudentId}
            onChange={(e) => setSelectedStudentId(Number(e.target.value))}
          >
            {students.map((s) => (
              <option value={s.id} key={s.id}>{s.name}</option>
            ))}
          </select>
        </div>
      </header>

      <section className="kpi-grid">
        <KpiCard label="Total Spending" value={`$${k.total_spending}`} />
        <KpiCard label="Transactions" value={k.transaction_count} />
        <KpiCard label="Average Transaction" value={`$${k.average_transaction}`} />
        <KpiCard label="Monthly Income" value={`$${k.monthly_income}`} />
        <KpiCard label="Budget Total" value={`$${k.budget_total}`} />
        <KpiCard label="Budget Used" value={`${k.budget_used_pct}%`} />
        <KpiCard label="Top Category" value={k.highest_spending_category} />
        <KpiCard label="Top Category Spend" value={`$${k.highest_category_amount}`} />
        <KpiCard label="Savings Goal" value={`$${k.savings_goal}`} />
        <KpiCard label="Current Savings" value={`$${k.current_savings}`} />
        <KpiCard label="Savings Progress" value={`${k.savings_progress_pct}%`} />
        <KpiCard label="Remaining Needed" value={`$${k.remaining_savings_needed}`} />
        <KpiCard label="Monthly Surplus" value={`$${k.estimated_monthly_surplus}`} />
        <KpiCard label="Savings Rate" value={`${k.savings_rate_pct}%`} />
        <KpiCard label="Categories Tracked" value={k.categories_tracked} />
        <KpiCard label="Budgets Created" value={k.budgets_created} />
      </section>

      <section className="charts-grid">
        <div className="chart-card">
          <h2>Spending by Category</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={dashboard.spending_by_category}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="category" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="amount" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h2>Monthly Spending Trend</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={dashboard.spending_by_month}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="amount" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h2>Budget Utilization</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={dashboard.budget_utilization}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="category" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="utilization_pct" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h2>Platform Category Mix</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={platform?.top_categories || []}
                dataKey="amount"
                nameKey="category"
                outerRadius={110}
                label
              >
                {(platform?.top_categories || []).map((_, index) => (
                  <Cell key={index} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="platform-card">
        <h2>Platform Overview</h2>
        <div className="platform-grid">
          <KpiCard label="Students Helped" value={platform?.total_students ?? 0} />
          <KpiCard label="Total Transactions" value={platform?.total_transactions ?? 0} />
          <KpiCard label="Platform Spending" value={`$${platform?.total_platform_spending ?? 0}`} />
          <KpiCard label="Avg Savings Progress" value={`${platform?.average_savings_progress_pct ?? 0}%`} />
        </div>
      </section>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
