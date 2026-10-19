# cw-remote-test

- Backend: FastAPI in `backend/main.py`, tests in `backend/tests/`. Run tests with `cd backend && uv run pytest -q`
  (no uv? `curl -LsSf https://astral.sh/uv/install.sh | sh`).
- Frontend: React 19 + TanStack Query v5 in `frontend/src/`; API calls only in `src/api.ts`. Check it with
  `cd frontend && npm install && npm run build`.
- Every backend change gets a test in `backend/tests/`. Keep both checks green before committing.
- Ports: on a shared machine use `$CW_PORT_BASE` for the API (`API_PORT=$CW_PORT_BASE`) and `$CW_PORT_BASE+1`
  for the dev server (`PORT=$((CW_PORT_BASE+1))`). Kill any server you start before you finish.
