import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'

import { createTodo, deleteTodo, listTodos, toggleTodo } from './api'

export function App() {
  const qc = useQueryClient()
  const todos = useQuery({ queryKey: ['todos'], queryFn: listTodos })
  const refresh = { onSuccess: () => qc.invalidateQueries({ queryKey: ['todos'] }) }
  const add = useMutation({ mutationFn: createTodo, ...refresh })
  const toggle = useMutation({ mutationFn: toggleTodo, ...refresh })
  const remove = useMutation({ mutationFn: deleteTodo, ...refresh })
  const [title, setTitle] = useState('')

  return (
    <main style={{ fontFamily: 'system-ui', maxWidth: 480, margin: '2rem auto' }}>
      <h1>Todos</h1>
      <form
        onSubmit={e => {
          e.preventDefault()
          if (title.trim()) add.mutate(title.trim(), { onSuccess: () => setTitle('') })
        }}
      >
        <input value={title} onChange={e => setTitle(e.target.value)} placeholder="What needs doing?" />
        <button type="submit" disabled={add.isPending}>Add</button>
      </form>
      {todos.isPending && <p>Loading…</p>}
      {todos.isError && <p role="alert">Could not load todos: {todos.error.message}</p>}
      <ul>
        {todos.data?.map(t => (
          <li key={t.id}>
            <label style={{ textDecoration: t.done ? 'line-through' : undefined }}>
              <input type="checkbox" checked={t.done} onChange={() => toggle.mutate(t.id)} /> {t.title}
            </label>{' '}
            <button onClick={() => remove.mutate(t.id)} aria-label={`delete ${t.title}`}>×</button>
          </li>
        ))}
      </ul>
    </main>
  )
}
