---
name: review-mr
description: Review an open pull/merge request with verify-before-trusting rigor — check claims against actual code and live state instead of trusting the diff's own docstrings and comments, separate real blockers from nitpicks with explicit reasoning, and confirm previously raised concerns actually got fixed rather than just touched. Use when the user wants to review a PR/MR, asks whether a fix actually solves the problem (vs. a symptom), or wants review feedback drafted and posted as PR/MR comments.
---

# Review MR

A review pass that trusts nothing it hasn't checked. The diff describes what changed; it does not prove the change is correct, complete, or placed in the right spot. This skill's job is closing that gap before anything gets approved.

## Hard dependency

Posting comments needs the tracker's exact CLI shape (`gh`/`glab`, how to view a diff, how to post a PR/MR comment). That mapping should have been provided to you — run `/setup-matt-pocock-skills` if not. Use the "Pull requests" / "Merge requests" section of `docs/agents/issue-tracker.md` (or wherever this repo's copy lives) for the exact commands — if that section is missing or thin, it's out of date; refresh it from `setup-matt-pocock-skills`'s seed docs (`issue-tracker-github.md` / `issue-tracker-gitlab.md`) before continuing.

## Soft dependencies

- The project's domain glossary (`CONTEXT.md`) and any architecture docs in the area being touched — read them before judging whether something is placed correctly.
- A repo-local `review-conventions.md` (wherever this repo's other agent config lives, e.g. `.claude/agents/` or `docs/agents/`) if one exists — repo-specific things like how to safely verify against production, and where follow-up tickets for out-of-scope findings should be filed. Works without it, just less sharp: fall back to asking the user before touching anything that looks like a production system.

## Process

1. **Fetch the MR/PR and its ticket.** Full diff, existing comments/threads, and the linked issue. Read the ticket's actual priority and intent, not just its title — a Priority::Low "stop an edge case" ticket earns a different bar than a Critical incident. If a prior review already raised concerns, read them before anything else.

2. **Read the diff in full**, not a summary. Note every claim the diff makes about itself: docstrings ("this is the backstop"), comments ("unbypassable", "handles X"), and the PR description's own account of what it fixes.

3. **Verify every load-bearing claim.** Don't accept a docstring's account of its own correctness. For each claim, ask "how would I know this is true" and go check:
   - Is this exception/error path ever actually caught, or would it surface as a raw 500/unhandled crash if it fired?
   - Does this code run for every real caller, or only the ones the author tested? Grep for other call sites.
   - Does the claimed "impossible" or "unreachable" state actually have zero instances? If a safe read-only check against production is possible per this repo's conventions, do it — don't assume.
   - If this is a fix for a previously-reported bug, does the new code actually address the reported symptom, or a related-but-different one? Re-derive it, don't infer from "the diff changed something in the right file."
   - If this closes a thread from an earlier review round, diff the current state specifically against what that comment asked for — confirm it, don't assume an update means it's resolved.

4. **Classify every finding.** Blocker or not — and say why in one sentence per finding, not a vague feeling:
   - **Blocker**: a claim in the code is actively false (misleading docstring/comment), a path is unreachable/dead by construction, a failure mode is unhandled, or the fix doesn't address the actual reported problem.
   - **Not a blocker**: style, redundant-but-harmless, could be cleaner. Say so if asked, but don't pad the review with it unprompted.
   - **Architecture violation, but shippable now**: the change works and fixes the immediate issue, but violates a documented project convention (rule of three, layering, module boundaries, etc.) in a way that's out of scope to fix in this MR. This is "approve on condition" territory, see step 6.

5. **Draft, don't post yet.** One overview comment: ticket context (priority/intent), a short numbered list of what's blocking and why, and a pointer to the detail comments. Then one separate comment per blocker/topic, so each can be discussed and resolved independently instead of buried in a wall of text. Use [TEMPLATES.md](TEMPLATES.md) for the exact shape. Keep it addressed to whoever wrote the code — assume good faith, state evidence, skip the lecture.

6. **Architecture violations get a condition, not a block.** If a finding is real but out of scope for this MR (wrong priority ticket to fix it in, small isolated fix that shouldn't grow), don't hold the MR hostage to it. Instead: draft a follow-up ticket capturing the violation and the suggested fix, get the user's go-ahead, file it, then reference its number in the review comment ("merging as-is on the condition that X is tracked in #NNN").

7. **Show the full draft to the user before posting anything.** Never post to a shared MR/PR autonomously. Once approved, post via the tracker's PR/MR comment command, overview first, then each detail comment in the order listed in the overview.

## Reference

- [TEMPLATES.md](TEMPLATES.md) — the overview / blocker / minor / suggested-approach comment shapes.
