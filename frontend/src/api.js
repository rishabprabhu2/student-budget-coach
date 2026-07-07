const API_BASE = "http://127.0.0.1:8000";

export async function getStudents() {
  const res = await fetch(`${API_BASE}/students`);
  return res.json();
}

export async function getStudentAnalytics(studentId) {
  const res = await fetch(`${API_BASE}/analytics/student/${studentId}`);
  return res.json();
}

export async function getPlatformAnalytics() {
  const res = await fetch(`${API_BASE}/analytics/platform`);
  return res.json();
}
