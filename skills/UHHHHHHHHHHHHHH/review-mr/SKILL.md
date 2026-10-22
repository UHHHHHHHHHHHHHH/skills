---
name: review-mr
description: Blunt one-shot review of an open pull/merge request: verify claims against real code and live state instead of trusting the diff's own docstrings, then report the load-bearing problem. Only user-facing and security/GDPR issues count. Use when the user explicitly wants findings handed to them without a walkthrough, or asks whether a fix solves the real problem rather than a symptom. For a normal review, use grill-mr instead, which walks them through it.
---

# Review MR

A review pass that trusts nothing it hasn't checked. The diff describes what changed; it does not prove the change is correct, complete, or placed in the right spot. This skill's job is closing that gap before anything gets approved.

This is the blunt version, for when the user wants findings without a conversation. `grill-mr` is the default: it walks them through the MR part by part so the understanding is theirs. Prefer that unless they asked for this one. Say once, at the start, what this mode costs them: they get a conclusion they weren't part of forming, and they'll have to judge it without having read the code.

## What counts as a problem

One question decides it: **would a user hit this, or is it a security, GDPR, or compliance problem?** Everything else is cleanup that can happen whenever.

Do not carry a list of things to look for. A named list of smells becomes a list of things you go find, and makes you blind to whatever isn't on it. Report what the change actually does wrong, not what it resembles.

Code quality findings are rare and reject-only. Three gates, all of which must pass:

1. **Can you name the concrete failure?** Not "fragile", but "when a second caller does X this returns the wrong date". If the sentence won't finish, it's taste. Drop it.
2. **Is it mechanically enforceable?** If a linter or import-boundary rule could catch it, the finding is "we're missing a rule". Suggest the rule as a ticket and drop it from the review.
3. **Does the cost of fixing it grow if this ships?** A migration, a data model, a public shape: worth a mention. Internal organisation is as cheap to fix next month. Drop it.

Zero quality findings is the normal outcome. One that survives is a trailing sentence on the finding it shares a cause with, or a follow-up ticket. Never its own thread, never an item in a numbered list of concerns.

## Evidence: prefer the product over the source

The strongest evidence is the running feature contradicting itself. It can't be argued with, it's already in the assignee's language, and it can be reproduced in front of them later. A screenshot beats a file reference. If the change touches a user-visible surface, exercise it using the scenario from the ticket before reading the diff for causes. The code-level root cause is what you attach to explain the observation, not the finding itself.

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

4. **Classify each finding** against the question above, and say why in one sentence. A blocker is user-facing or a security/GDPR problem. Something real but out of scope (works, fixes the immediate issue, but violates a documented convention this MR shouldn't grow to fix) is "approve on condition" territory, see step 6. Everything else was already dropped by the gates.

5. **Report, don't draft.** Lead with the single most load-bearing finding, stated in one sentence with its evidence. Not a numbered pile: a numbered list makes the reader sort signal from noise, which is the work this skill was supposed to do for them. If there are others, say how many and what they are in one line each, under the first. Say plainly what you checked and what you didn't. Then stop and let the user decide what to do with it.

   Draft comments only if they ask. Shape: the observation in domain language, what the user ends up seeing, and the evidence attached. Short. No prefix labels, no `Fix:` section, no scaffolding — write it the way a colleague would type it. One comment per problem so each can be discussed on its own, addressed to whoever wrote the code: good faith, evidence, no lecture. Show one and wait before writing the next.

6. **Architecture violations get a condition, not a block.** If a finding is real but out of scope for this MR (wrong priority ticket to fix it in, small isolated fix that shouldn't grow), don't hold the MR hostage to it. Instead: draft a follow-up ticket capturing the violation and the suggested fix, get the user's go-ahead, file it, then reference its number in the review comment. Cite the convention being broken and name how many times the exception has now been made — the rule of three matters, and "third time we've done this" is a different argument than "this is untidy". Then say plainly that it's merging as-is because the risk of leaving the issue unfixed outweighs the cleanliness cost, on the condition that the proper fix lands as a followup, tracked in #NNN.

7. **Show every draft to the user before posting anything.** Never post to a shared MR/PR autonomously. Once approved, post via the tracker's PR/MR comment command.
