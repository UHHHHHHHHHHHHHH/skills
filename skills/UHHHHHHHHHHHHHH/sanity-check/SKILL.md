---
name: sanity-check
description: Force Claude to critically re-examine its own assumptions, verify code correctness, and validate claims. Use when Claude made an assumption, wrote code that "should work", gave a confident answer you want double-checked, or anytime you want Claude to stop and verify before moving on. Trigger words - sanity check, double check, are you sure, verify that, check yourself, does this actually work.
---

# Sanity Check

You have been asked to perform a sanity check. This means the user wants you to STOP, step back, and critically re-examine your recent work or claims. Do not be defensive. Do not hand-wave. Be brutally honest.

## Core Protocol

Follow ALL of these steps. Do not skip any.

### Step 1: Identify What to Check

Look at the conversation context and determine what needs sanity-checking. This is usually one or more of:

- **An assumption you made** (about how something works, what exists, what's compatible)
- **Code you just wrote** (does it actually work? did you forget something?)
- **A claim you made** (is it actually true? are you confusing something?)
- **A plan you proposed** (will it actually work end-to-end?)

If the user said `/sanity-check` with additional context (e.g., `/sanity-check the database query`), focus on that specific thing. Otherwise, check everything from your most recent substantive response.

### Step 2: List Your Assumptions

Write out every assumption you made, explicitly. Number them. Be thorough. Examples:

- "I assumed the function `foo()` exists in `bar.py`"
- "I assumed this API returns JSON"
- "I assumed Python 3.10+ is available"
- "I assumed this import path is correct"
- "I assumed this field exists on the model"
- "I assumed these two things are compatible"

### Step 3: Verify Each Assumption

For each assumption, **actually verify it**. Do not just think about it — use your tools:

- **File/function exists?** → Use Glob or Grep to find it
- **Import path correct?** → Read the actual module to confirm exports
- **API behavior?** → Read the source, check docs, or look at existing usage in the codebase
- **Config/env assumption?** → Check the actual config files
- **Syntax correct?** → Look at similar working examples in the codebase
- **Types/fields exist?** → Read the model/schema definition
- **Dependencies available?** → Check package.json, requirements.txt, pyproject.toml, etc.
- **Logic correct?** → Trace through edge cases mentally, or find tests

Mark each assumption as: **VERIFIED**, **WRONG**, or **UNVERIFIABLE** (with explanation).

### Step 4: Check for Common Pitfalls

Explicitly check for these frequent mistakes:

- [ ] **Hallucinated APIs/functions**: Did you reference a function, method, flag, or parameter that doesn't actually exist?
- [ ] **Wrong import paths**: Is the import you used the actual path in this project?
- [ ] **Version mismatches**: Are you using syntax/features from a newer version than what's installed?
- [ ] **Missing error handling**: Will this blow up on edge cases the user will hit?
- [ ] **Wrong mental model**: Are you thinking of how a *different* framework/library does this?
- [ ] **Copy-paste errors**: Did you reuse code but forget to update variable names, paths, or values?
- [ ] **Incomplete solution**: Does this actually solve the whole problem, or just part of it?
- [ ] **Side effects**: Will this change break something else?
- [ ] **Environment assumptions**: Are you assuming something about the OS, shell, installed tools, or runtime?
- [ ] **Off-by-one / boundary errors**: Are loops, slices, ranges, and conditions correct at boundaries?

### Step 5: Deliver the Verdict

Present your findings clearly:

```
SANITY CHECK REPORT
═══════════════════

Checked: [what you checked]

Assumptions:
  1. [assumption] → VERIFIED / WRONG / UNVERIFIABLE
  2. [assumption] → VERIFIED / WRONG / UNVERIFIABLE
  ...

Issues Found:
  - [issue description and what's wrong]
  - [issue description and what's wrong]
  ...

Verdict: ALL CLEAR / ISSUES FOUND / NEEDS MORE INVESTIGATION
```

### Step 6: Fix or Flag

- If you found issues: **fix them immediately** (don't just report — actually correct the code/plan/claim)
- If you can't verify something: **say so clearly** and explain what information you'd need
- If everything checks out: **confirm with specifics** about what you verified and how

## Important Rules

1. **No rubber-stamping.** Don't just say "looks good!" — actually verify things with tools.
2. **Be specific.** "I think this is fine" is not a sanity check. Show your work.
3. **Check the actual codebase.** Don't verify assumptions from memory — read the files.
4. **Admit mistakes.** If you got something wrong, say so plainly. No hedging.
5. **Verify before claiming.** If you say "VERIFIED", you must have actually looked at the source.
6. **Include confidence levels.** For each finding, state how confident you are.

## Usage Examples

```
User: [asks Claude to add a new API endpoint]
Claude: [writes the endpoint code]
User: /sanity-check

→ Claude re-examines: Does the router actually use this pattern? Do the imports exist?
  Does the model have these fields? Is the auth middleware applied correctly?
```

```
User: /sanity-check the migration
→ Claude verifies: Is the SQL valid? Do the referenced tables/columns exist?
  Will this break existing data? Is it reversible?
```

```
User: [Claude explains how something works]
User: /sanity-check
→ Claude re-reads the actual source code to verify its explanation is correct
```
