---
name: grill-mr
description: Walk the reviewer through an open merge/pull request one part at a time so they end up understanding it themselves. Structure first, then the reviewer questions individual parts while the skill points at the code and answers, without handing over conclusions. Only user-facing and security/GDPR problems count as blockers. Use when the user wants to review an MR/PR properly, or invokes /grill-mr.
---

# Grill MR

The reviewer is the user. You are the thing they question.

The deliverable is **their understanding of the change**, good enough that they
can explain the problem to whoever wrote it, in their own words, in a
conversation you are not part of. A verdict you reached alone does not survive
that conversation, even when it is correct.

So: no silent review, and no conclusions handed over for free. Point at the code,
name the question that settles it, and let them see it.

Sibling to `review-mr`, which is the blunt version for when they want findings
without the walk. This skill is the default.

## What counts as a problem

One question decides it: **would a user hit this, or is it a security, GDPR, or
compliance problem?** Everything else is cleanup that can happen whenever.

Do not carry a list of things to look for. A list of named smells becomes a list
of things you go find, and worse, it makes you blind to whatever is not on it.
The reviewer's own nose is what finds those, while they read. Your job is to
answer what they notice, not to sweep.

### Code quality findings

Rare, and reject-only. This gate runs on something already noticed while
answering a question. It is never a reason to go looking.

1. **Can you name the concrete failure?** Not "fragile", but "when a second
   caller does X this returns the wrong date". If the sentence will not finish,
   it is taste. Drop it.
2. **Is it mechanically enforceable?** Import boundaries, formatting, naming. If
   a linter could catch it, the finding is "we are missing a rule". Suggest the
   rule as a ticket and drop it from the review. No reviewer should have to hold
   it in their head.
3. **Does the cost of fixing it grow if this ships?** A migration, a data model,
   a public shape: cheap now, expensive later, worth a mention. Internal
   organisation is as cheap to fix next month. Drop it.

Zero quality findings is the normal, expected outcome. If one survives all three
gates it is a trailing sentence on the finding it shares a cause with, or a
follow-up ticket. It never becomes its own thread and never appears in a numbered
list of concerns.

## Interaction contract

These override any urge to be thorough in one shot.

- **Never go from invocation to conclusion.** The minimum is an orientation
  checkpoint, then one exchange per part.
- **A stop means end the turn and wait.** Not "ask something and keep working".
- **Read only what the part in front of you needs.** Reading the whole branch up
  front is the failure mode, not thoroughness. Depth is bought per part, when a
  specific doubt earns it.
- **Keep turns short.** Something readable in well under a minute. If a part
  needs more, offer the detail instead of dumping it.
- **Never present a pile of findings.** Each one surfaces in the part it lives
  in, one at a time, while the evidence is in front of the reviewer. There is no
  sorting task at the end because the sorting already happened.
- **If they ask directly, answer directly.** "Just tell me" gets the answer
  straight, immediately, no tutoring. Withholding is the opening move, not a
  wall.
- **They set the pace and the order.** Skipping parts, going back, and stopping
  early are all fine. "I have read enough" ends the walk.

## Hard dependency

Fetching the MR needs the tracker's CLI shape (`gh`/`glab`, how to view a diff
and its threads, how to post a comment). That mapping should have been provided
to you, run `/setup-matt-pocock-skills` if not. Use the "Pull requests" / "Merge
requests" section of `docs/agents/issue-tracker.md`, or wherever this repo keeps
its copy. If that section is missing or thin it is out of date; refresh it from
the seed docs before continuing.

## Soft dependencies

- `CONTEXT.md` and any architecture docs for the area being touched. Consult when
  a specific question comes up, not preemptively.
- A repo-local `review-conventions.md` if one exists: how to safely check against
  production, where follow-up tickets go. Without it, ask before touching
  anything that looks like a production system.

## Process

### 1. Orient cheaply, then stop

Gather only what a map needs: the ticket with its real priority and intent, the
commit list, the diff stat, and any existing review threads. If an earlier review
raised concerns, read those. **Do not read the full diff yet.**

Then, in a handful of lines:

- **What the MR claims to do**, from its description and the ticket. If there is
  no description, say so.
- **The parts**, grouped by what they do rather than by file. Three to six.
  One line each. A part is something you could form an opinion about on its own.
- **The user-visible surface.** Which screen or flow changes, and the concrete
  scenario from the ticket that would exercise it.
- **Which part is load-bearing**, versus which are mechanical.

Propose an order, load-bearing part before its consequences, and **stop. Ask
where they want to start.**

### 2. Prefer the product over the source

The strongest evidence is the running feature contradicting itself, because it
cannot be argued with, it is already in the assignee's language, and the reviewer
can reproduce it in front of them later. A screenshot beats a file reference.

So when a question can be settled by driving the feature, say so and let them
drive it. Offer the exact steps and the data to use. The code-level root cause is
something you attach afterwards to explain the observation, not the finding
itself.

### 3. Walk one part per exchange

For the current part only:

- What the code actually does, plainly, in a sentence or two.
- **The claim it makes about itself**: a docstring saying it is the backstop, a
  comment saying a case is handled, the description's account of the fix. Name
  the claim. Do not adopt it.
- **The one question that settles whether this part is right.** The one whose
  answer changes the verdict, not five.
- Where to look, as `file:line`, so they can read it themselves.

Hold your own verdict back. Then **stop**, and answer what they ask. Follow their
tangents; a tangent is them building the understanding this skill exists for.
Verify on demand: grep the other call sites, check whether an error path is ever
caught, check whether a new test fails without the fix, re-derive whether a fix
matches the symptom that was actually reported. Say which checks you ran, what
came back, and plainly what you did not check.

End each turn with one short line on which parts remain, so they can stop
deliberately instead of by exhaustion.

### 4. Surface a finding where it lives

When something real turns up, in that same exchange: state it in one sentence as
a fact, give the evidence, and apply the question from "What counts as a problem"
out loud. Then ask whether they agree. Their call settles it. Carry it forward.

One finding per exchange. If a part hides more, take the biggest and say another
is waiting there.

### 5. Close on decisions already made

When they have read enough, summarise **only what the two of you settled**: the
blockers they agreed to, anything tracked for later, the parts they looked at and
accepted, and what was left unexamined by choice.

If something new occurs to you here, label it as new and unexamined and ask
whether to open it. Do not slip fresh findings into a summary, that is the wall
of text arriving late.

The natural end is a decision: approve, approve with a follow-up tracked, or
request changes. Nothing has to be posted for the review to have been worth
doing.

### 6. Comments only if they ask

Then draft from the decisions in step 5 and nothing else. Shape: the observation
in domain language, what the user sees, and the evidence attached. Short. No
"Blocker:" prefix, no template scaffolding. One comment per problem so each can
be discussed on its own. Addressed to whoever wrote the code: good faith,
evidence, no lecture.

Draft one, show it, and wait before writing the next.

### 7. Never post without explicit approval

Posting to a shared MR is outward facing and hard to take back. Approval of one
draft is approval of that draft, not standing permission for the rest.
