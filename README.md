# cw-remote-test

A tiny todo app for trying cheap-worker's remote workers: a FastAPI API (`backend/`) and a
React + TanStack Query frontend (`frontend/`). Todos live in memory, so a restart empties them.

## Run it

```sh
cd backend && uv run uvicorn main:app --reload --port ${API_PORT:-8000}
cd frontend && npm install && npm run dev      # http://localhost:5173, proxies /api to the API
```

## Test it

```sh
cd backend && uv run pytest -q
cd frontend && npm run build                   # type-check and bundle
```
