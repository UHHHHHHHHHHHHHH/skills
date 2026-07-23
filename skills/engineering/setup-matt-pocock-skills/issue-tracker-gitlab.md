# Issue tracker: GitLab

Issues and PRDs for this repo live as GitLab issues. Use the [`glab`](https://gitlab.com/gitlab-org/cli) CLI for all operations.

## Conventions

- **Create an issue**: `glab issue create --title "..." --description "..."`. Use a heredoc for multi-line descriptions. Pass `--description -` to open an editor.
- **Read an issue**: `glab issue view <number> --comments`. Use `-F json` for machine-readable output.
- **List issues**: `glab issue list -F json` with appropriate `--label` filters.
- **Comment on an issue**: `glab issue note <number> --message "..."`. GitLab calls comments "notes".
- **Apply / remove labels**: `glab issue update <number> --label "..."` / `--unlabel "..."`. Multiple labels can be comma-separated or by repeating the flag.
- **Close**: `glab issue close <number>`. `glab issue close` does not accept a closing comment, so post the explanation first with `glab issue note <number> --message "..."`, then close.

Infer the repo from `git remote -v` — `glab` does this automatically when run inside a clone.

## Merge requests

GitLab calls PRs "merge requests".

- **Find the MR for a branch**: `glab mr list --source-branch <branch>`.
- **View metadata + description**: `glab mr view <number> --comments`.
- **Full diff**: `glab mr diff <number>`.
- **Post a general MR comment (a "note")**: `glab mr note <number> --message "..."` (heredoc for multi-line). Newer `glab` deprecates `--message` in favor of `glab mr note create`; either works, use whichever the installed version doesn't warn on.
- **Post a comment anchored to a specific file/line**: not supported by `glab mr note`; requires the GitLab REST API directly (`glab api projects/:id/merge_requests/:iid/discussions`) with position data. Prefer a general note referencing `file.py:123` in the text unless line-anchoring is specifically required — far less brittle.
- **Approve**: `glab mr approve <number>`. GitLab has no separate "request changes" state — an unresolved thread, or a comment saying so explicitly, is the convention.

## When a skill says "publish to the issue tracker"

Create a GitLab issue.

## When a skill says "fetch the relevant ticket"

Run `glab issue view <number> --comments`.
