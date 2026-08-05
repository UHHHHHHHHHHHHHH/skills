# My own skills

This category holds skills I wrote from scratch. The rest of the repo is Matt
Pocock's work, credit to him for those and for the structure and ideas.

I also customize his skills in place when his defaults don't fit my workflow
(the issue-tracker setup is the likely first one, for `to-mr`). So his files may
carry my changes; those customizations are mine, the original is still his.

## About this repo

It's a fork of [mattpocock/skills](https://github.com/mattpocock/skills) (MIT).
Pull his updates with:

    git fetch upstream
    git merge upstream/main

Any of his files I've customized may need a small merge when he changes the same
ones. That's expected and only affects what I touched. Skills I wrote from
scratch live here under `skills/UHHHHHHHHHHHHHH/`, in their own files, so they
don't collide with his at all.

## Skills

- [start-ticket](start-ticket/SKILL.md): start work on a GitLab ticket, create
  the branch, bookmark the session for claude-resume
- [grill-mr](grill-mr/SKILL.md): walk through an open MR part by part, questions
  first, so the understanding ends up being mine
- [review-mr](review-mr/SKILL.md): the blunt sibling of `grill-mr`, for findings
  without the walk
- [sanity-check](sanity-check/SKILL.md): force a critical re-examination of
  recent assumptions, claims, and "should work" code
- [to-mr](to-mr/SKILL.md): open an MR/PR for the current branch, linked to its
  ticket with a non-closing reference; defers all CLI to the repo's
  issue-tracker doc
