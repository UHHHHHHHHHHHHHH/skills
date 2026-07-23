---
name: start-ticket
description: Start work on a ticket from a GitLab issue URL. Creates a branch for it and bookmarks the (ticket, session, directory, branch) mapping so claude-resume can jump back into this exact chat later. Use when the user invokes /start-ticket with a ticket URL.
---

# Start Ticket

Kick off work on a ticket. The two jobs that matter: create a branch, and write
the bookmark that lets [`claude-resume`](https://github.com/UHHHHHHHHHHHHHH/claude-resume)
find this session again.

Run from the repo/checkout where the work will live. The user passes a GitLab
issue URL as the argument.

## Process

### 1. Parse the URL

Pattern: `https://<gitlab-host>/<namespace>/<project>/-/(issues|work_items|merge_requests)/<number>`

`work_items` is GitLab's newer URL for the same thing; `glab issue view <n>`
works for those too.

The bookmark key is `<project>/<number>`. Note the ticket may live in a
different project than the repo you are in (e.g. an intake/support project whose
issues are worked on in a separate code repo). That is fine: the key comes from
the URL, the cwd/branch from where you are.

If no argument was given, first thing you do is ask: what's the ticket, brother?
A URL is preferred, but a bare number works too if the project is obvious from
the cwd (confirm which project you assumed). If the argument is something else
entirely, ask for a URL rather than guessing.

### 2. Fetch the ticket

`glab issue view <number> -R <namespace>/<project> --comments`

Read the title and body so you understand what the ticket is about.

### 3. Propose a branch name

If the repo declares a branch naming convention (CLAUDE.md, CONTRIBUTING,
wherever), follow it. Otherwise a readable slug of the ticket title is fine.
Either way PROPOSE the name to the user before creating anything and let them
edit or replace it.

Conventions are per-repo and ticket numbers are per-tracker-project. If the
work happens in a DIFFERENT repo than the one the ticket belongs to (e.g. the
ticket is in the app's tracker but the fix is in a dependency repo), do NOT
prefix that repo's branch with the ticket number; there it's meaningless or
collides with that repo's own issue numbers. Use a plain slug, or reference the
origin explicitly like `<origin-project>-<number>-<slug>` if the user wants
traceability.

Also confirm the base. Default to the repo's default branch, NOT the current
HEAD: in a worktree the current HEAD is often the previous ticket's branch.
Derive the default with `git symbolic-ref refs/remotes/origin/HEAD` (gives
`origin/<default>`). Mention what HEAD currently is so the user can choose it
deliberately if they want to stack.

### 4. Create the branch

`git checkout -b <approved-name> origin/<base> --no-track`

Fetch first (`git fetch origin`) so the branch starts from the latest remote
state, not a stale local one. `--no-track` matters: without it the new branch
tracks `origin/<base>`, and a later `git push` would target the protected base
branch instead of publishing the feature branch. First push is
`git push -u origin HEAD`.

If the working tree is dirty, tell the user and let them decide (stash, commit,
or abort) instead of proceeding.

#### If the app mounts sibling repos (dependency worktrees)

Some repos run the app with sibling/dependency repos mounted in as live volumes.
If the work needs a branch in one of those, that checkout must be isolated from
the main checkout, otherwise resuming one ticket flips a branch out from under
another running stack that has the same dependency mounted.

The specifics (which repos are mounted, where the isolated per-worktree
checkouts live, how the mount is wired) are per-repo and not derivable, so they
live in a repo-local doc, `worktree-setup.md`, wherever this repo keeps agent
config (`.claude/agents/`, `docs/agents/`). See
[worktree-setup.template.md](worktree-setup.template.md) for its shape.

- No such doc and nothing suggests mounted siblings -> single-repo ticket, do
  nothing special here.
- The doc exists -> follow it: create the dependency branch in the isolated
  worktree it names, work there, and bookmark that path in step 5.
- The pattern applies (the user says the app mounts a sibling repo) but no doc
  exists yet -> offer to set it up once: create the isolated worktree, wire the
  mount as the doc describes, and write `worktree-setup.md` from the template so
  next time it is automatic.

Cross-repo branch naming (step 3) applies to the dependency branch too.

### 5. Write the bookmark

Run:

    claude-resume bookmark <project>/<number>

It records `(key, session, cwd, branch)` itself: the session is this live chat
(newest transcript), the cwd defaults to the current directory, and the branch
to whatever is checked out there. Run it FROM the checkout where the branch you
just made lives, so those defaults are right. It prints back what it wrote,
confirm the four fields look correct.

If the ticket spans repos (a branch in the app repo AND one in a dependency
repo), call it once per repo with explicit overrides so each row points at that
repo's checkout:

    claude-resume bookmark <project>/<number> <other-repo-abs-path> <other-branch>

Same key and session for all rows (one chat drives them); only cwd and branch
differ. Create the dependency branch BEFORE writing its row: bookmark verifies
the branch exists in that checkout and refuses the row otherwise.

Rows are keyed on (key, cwd), so re-bookmarking a repo replaces its row rather
than stacking a second one. On resume the winner is the row whose cwd is where
this chat is running, not the newest row, so the extra rows are metadata for
other tools rather than alternative landing spots.

### 6. Start the work

TODO: this is where the actual ticket-start instructions go (context
gathering, exploring the affected code, drafting an approach). For now:
summarize the ticket in a few lines and ask the user where they want to
begin.
