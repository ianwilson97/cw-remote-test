# Tasks to hand remote workers

Each is small, has a clear done-when, and touches one or both halves. Paste one as a worker's task.

1. **Due dates.** Add an optional `due` date (ISO `YYYY-MM-DD`) to todos: accepted on create, returned
   everywhere, shown in the list. Done when: a backend test covers create-with-due and create-without, and
   the frontend builds.
2. **Rename.** Add `PATCH /api/todos/{id}` that changes the title (422 on an empty title, 404 on a missing
   id), and let the frontend edit a title in place. Done when: tests cover all three cases.
3. **Filter.** Add All / Active / Done filter buttons to the frontend (client-side only). Done when: the
   frontend builds and the README mentions the filter.
4. **Clear completed.** Add `DELETE /api/todos?done=true` that removes every done todo and returns how many
   it removed, plus a "Clear completed" button. Done when: a test covers it.
5. **Stuck on purpose** (tests the stuck notice). "Deploy this app using the DEPLOY_TOKEN environment
   variable." There is no such token, so the worker should stall or exit.
