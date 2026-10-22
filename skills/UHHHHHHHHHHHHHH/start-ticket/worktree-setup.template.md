# worktree-setup.md (template)

Copy this into a repo that runs its app with sibling/dependency repos mounted in,
and fill in the specifics. Put the filled copy where the repo keeps agent config
(`.claude/agents/worktree-setup.md` or `docs/agents/worktree-setup.md`).
`/start-ticket` reads it to isolate dependency branches per worktree instead of
fighting over one shared checkout. If a repo has no such doc, the skill treats
tickets as single-repo and does nothing special.

This template stays generic and public; the FILLED copy naming your real repos
and paths lives in the (private) repo it describes, not in the skills repo.

Leave out any section that does not apply. The skill reads prose, not a schema,
so keep it readable.

---

## Mounted dependency repos

The app in this repo mounts these sibling repos as live volumes (so the running
app uses whatever branch each is checked out on):

- `<dep-repo-name>` at `<path-to-its-canonical-checkout>`
- ...

## The isolation rule

A running app plus its mounted dependencies is one unit. Keep them from
colliding across checkouts:

- The MAIN checkout (`<path>`) uses the canonical dependency checkouts above.
- Each parallel worktree of the app uses its OWN dependency checkouts, as git
  worktrees, so nothing it does touches the main checkout's dependencies.

## Where the isolated dependency worktrees live

One linked worktree per dependency repo, under a fixed folder:

    <worktree-deps-parent>/<dep-repo>

Create one with:

    git -C <path-to-canonical-dep-checkout> worktree add <worktree-deps-parent>/<dep-repo> <branch>

## How the mount is wired

The app worktree's `<mount-config-file>` (e.g. a docker-compose override) points
its dependency mounts at `<worktree-deps-parent>/<dep-repo>` instead of the
canonical checkout. This is a ONE-TIME edit at setup; after that the mount never
changes, only the branch checked out inside the worktree changes per ticket.

If that config file is tracked but must never be committed, it is usually hidden
with `git update-index --skip-worktree <file>` (or lives in a gitignored
override). Note here whichever this repo uses, and any gotcha (e.g. `git pull`
refusing with "local changes would be overwritten" while status looks clean,
because of skip-worktree).

## Notes for start-ticket

- Dependency branches follow the cross-repo naming rule: no originating ticket
  number prefixed onto the dependency repo's branch unless traceability is
  explicitly wanted.
- One ticket is active in the app worktree at a time, so a single dependency
  worktree flipping branches per ticket is fine.
