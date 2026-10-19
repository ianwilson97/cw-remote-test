export type Todo = { id: number; title: string; done: boolean }

async function call<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`/api${path}`, { headers: { 'content-type': 'application/json' }, ...init })
  if (!res.ok) throw new Error(`${init?.method ?? 'GET'} ${path}: ${res.status}`)
  return (res.status === 204 ? undefined : await res.json()) as T
}

export const listTodos = () => call<Todo[]>('/todos')
export const createTodo = (title: string) => call<Todo>('/todos', { method: 'POST', body: JSON.stringify({ title }) })
export const toggleTodo = (id: number) => call<Todo>(`/todos/${id}/toggle`, { method: 'PATCH' })
export const deleteTodo = (id: number) => call<void>(`/todos/${id}`, { method: 'DELETE' })
