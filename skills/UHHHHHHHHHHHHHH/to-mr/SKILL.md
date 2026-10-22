---
name: to-mr
description: Open a merge/pull request for the current branch and link it to its ticket with a NON-closing reference, so the tracker surfaces the branch on the issue without auto-closing it on merge. Seeds title and description from the ticket. Supports a draft mode for opening the MR mid-work. Use when the user wants to create/open/draft an MR or PR, or invokes /to-mr.
---

# To MR

Own the one thing every merge request must get right: it is linked back to its
ticket, and linked in a way that does NOT close the ticket when it merges. Where
the actual commands live is the tracker's business (see the dependency below);
this skill carries the discipline, not the CLI.

Sibling to `to-issues` / `to-prd`: MR creation routes here so the linking rule
lives in one distributable place instead of being re-derived per repo.

## Hard dependency

The exact CLI shape (`gh`/`glab`, how to push, how to create an MR/PR, the
default target branch, how to reference an issue across projects) comes from
this repo's `issue-tracker.md`, under its "Merge requests" / "Pull requests"
section. That mapping should have been provided to you, run
`/setup-matt-pocock-skills` if not. If that section is missing or thin it is out
of date; refresh it from the seed docs (`issue-tracker-github.md` /
`issue-tracker-gitlab.md`) before continuing. Never hardcode a command this doc
should be telling you.

## Soft dependencies

- The ticket the branch belongs to. If the user did not name it, try to resolve
  it (see step 2) before asking.
- A repo-local convention doc (`.claude/agents/`, `docs/agents/`, wherever this
  repo keeps agent config) for MR title/description house style, if one exists.

## Process

1. **Establish the branch and get it pushed.** Confirm the current branch is a
   real feature branch, not the protected main branch. Make sure it is published
   to the remote (push with upstream set) so there is something to open the MR
   from. If the working tree has uncommitted work the MR should include, tell the
   user and let them commit first, do not silently open an MR that omits it.

2. **Resolve the ticket.** The MR must reference one.
   - If the user passed a ticket URL/number, use it.
   - Otherwise reverse-look-up the current branch in the claude-resume bookmark
     file (`~/.config/claude-resume/bookmarks`, tab-separated
     `key<TAB>session<TAB>cwd<TAB>branch`): a row whose branch matches the
     current branch gives the ticket key `<project>/<number>`.
   - If neither resolves it, ASK the user for the ticket rather than opening an
     unlinked MR.

3. **Read the ticket** so title and description are grounded in it, not guessed.
   Use the tracker's issue-view command from `issue-tracker.md`. Note the ticket
   may live in a different project than this repo (e.g. an app-tracker ticket
   worked on in a dependency repo), that is expected and drives the reference
   format in the next step.

4. **Build the NON-closing reference.** This is the point of the skill.
   - Reference the issue so the tracker records the MR as related, but use the
     plain mention form, NEVER a closing keyword (`Closes`, `Fixes`, `Resolves`).
     A closing keyword would auto-close the ticket when the MR merges; we want the
     link without the close.
   - If the MR's repo differs from the ticket's project, use the tracker's
     cross-project reference form (full project path, or the full issue URL),
     per `issue-tracker.md`. A same-project ticket can use the short form.
   - Why non-closing matters beyond not closing early: it is what lets the ticket
     become the source of truth for every branch across every repo that belongs
     to it. An app ticket fixed partly in a dependency repo ends up with both MRs
     linked on the one issue, which is what a later multi-repo resume reads back.

5. **Seed title and description from the ticket.** Title: a readable summary of
   the change (start from the ticket title, refine to what the branch actually
   does). Description: a short account of the change, plus the non-closing
   reference line. PROPOSE both to the user and let them edit before anything is
   created.

6. **Draft mode when asked.** If invoked as `/to-mr draft` (or the user says the
   work is mid-flight), open the MR as a draft/WIP using the tracker's draft
   flag. Same linking rules apply, the reference goes in from the start so the
   ticket shows the branch even while the work is unfinished.

7. **Confirm before creating.** An MR is outward-facing and visible to the team.
   Show the final target branch, title, and description, and get the user's go
   before running the create command. After it is created, print the MR URL.
