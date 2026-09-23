export async function submitTask(description: string) {
  const res = await fetch('http://localhost:8000/tasks/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ description })
  });
  return res.json();
}
