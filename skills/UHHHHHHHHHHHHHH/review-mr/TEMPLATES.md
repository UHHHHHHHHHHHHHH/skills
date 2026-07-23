# Review comment templates

Post one overview comment, then one separate comment per finding. Never combine
findings into a single wall of text — each comment is its own thread so a reader
can resolve or push back on one issue without wading through the others.

## Overview comment

Goes first. Gives context, states the verdict, and points at what follows.

```
Context: [ticket priority/intent in one or two sentences — what this is actually
for, quoting the ticket if it clarifies scope]. [State any verification already
done, e.g. "nothing here is broken in production today: I checked directly and
found zero instances of X."]

[One sentence: is the core change right or wrong.] Where [the specific problem
area] needs work before I can approve it. [N] separate threads below:
1. [one-line summary of finding 1]
2. [one-line summary of finding 2]
...

[If applicable: "Plus one comment at the end with the approach I'd suggest instead."]
```

## Blocker comment

One per finding. Bold headline states the defect as a fact, not a question.

```
**Blocker: [one-sentence defect statement].**
[Why it's true — the evidence. File:line references, repro output, a prod query
result, a grep showing other callers. Concrete, not "this seems risky."]

Fix: [the specific, actionable change].
```

## Minor/nitpick comment

Only post these if they're concrete and evidenced — not a style preference dressed
up as a finding. No bold headline; these aren't blockers.

```
[What's duplicated/inconsistent and where, with file references.]

Fix: [specific suggestion]. [If it's tied to a blocker elsewhere: "see the comment
on X for the bigger picture."]
```

## Suggested approach (summary/closing comment)

Only when there's a coherent alternative shape worth spelling out, not just a list
of complaints. Goes last.

```
[One or two sentences naming the core mechanism of the correct approach.]

Concretely, this MR should end up removing:
- [thing 1] (comment N)
- [thing 2] (comment N)

and keeping/adding:
- [thing 3]
```

## Approve-with-condition (architecture violation, out of scope)

Used when the fix is correct and should ship, but violates a documented
convention that's a real followup, not a blocker.

```
This violates [the documented convention, cite the doc]: [one sentence on why].
[State how many times this exception has now been made — rule of three matters:
name each instance.]

Merging as-is since it correctly fixes the issue and the risk of leaving it
broken outweighs the cleanliness cost, but on the condition that the proper fix
lands as a followup: [the concrete right shape]. Tracked in #[issue].
```
