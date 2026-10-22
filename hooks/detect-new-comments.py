#!/usr/bin/env python3
"""Pre/PostToolUse hook for Write|Edit (invoked as "... pre" / "... post").

Blocks when an individual edit adds comment lines, so the "write zero
comments by default" rule in global CLAUDE.md self-enforces instead of
relying on the user to catch it and ask for removal every time.

Scoped to a before/after snapshot of just this one edit. Python files
get two extra passes: ast finds real docstring spans (module/class/
function first-statement string literals) so touching one, even
without adding a new comment-marker line, still flags; a triple-quote
toggle scan finds every OTHER triple-quoted string (plain content,
e.g. a note-generation script) so those stay exempt even though they
look identical to a docstring syntactically.
"""
import ast
import difflib
import hashlib
import json
import os
import re
import sys

COMMENT_RE = re.compile(r"^\s*(#|//|/\*|\*[^/]|\"\"\"|''')")


def triple_quote_state_per_line(lines):
    """True for each line index if it starts already inside an open
    triple-quoted string (naive toggle, ignores escaping)."""
    state = False
    quote = None
    result = []
    for line in lines:
        result.append(state)
        s = line
        while True:
            pos_d = s.find('"""')
            pos_s = s.find("'''")
            candidates = [p for p in (pos_d, pos_s) if p != -1]
            if not candidates:
                break
            pos = min(candidates)
            marker = '"""' if s[pos:pos + 3] == '"""' else "'''"
            if not state:
                state, quote = True, marker
            elif quote == marker:
                state, quote = False, None
            s = s[pos + 3:]
    return result


def docstring_line_indices(source, line_count):
    """0-indexed line numbers covered by a real docstring: the first
    statement of the module, or of any class/function, when it's a
    bare string literal. Returns an empty set on a parse error (file
    mid-edit or not valid Python)."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()

    nodes = [tree] + [
        n for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    ]
    covered = set()
    for node in nodes:
        body = getattr(node, "body", None)
        if not body:
            continue
        first = body[0]
        value = getattr(first, "value", None)
        if isinstance(first, ast.Expr) and isinstance(value, ast.Constant) and isinstance(value.value, str):
            start = first.lineno
            end = getattr(first, "end_lineno", first.lineno)
            covered.update(range(start - 1, min(end, line_count)))
    return covered


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "post"
    data = json.load(sys.stdin)
    tool_input = data.get("tool_input") or {}
    tool_response = data.get("tool_response") or {}
    file = tool_input.get("file_path") or tool_response.get("filePath")
    if not file or file.endswith(".md"):
        return

    cache_dir = os.path.expanduser("~/.cache/claude-comment-hook")
    os.makedirs(cache_dir, exist_ok=True)
    key = hashlib.sha256(file.encode()).hexdigest()
    snapshot = os.path.join(cache_dir, key)

    if mode == "pre":
        content = open(file, "rb").read() if os.path.isfile(file) else b""
        with open(snapshot, "wb") as f:
            f.write(content)
        return

    if not os.path.isfile(file):
        return
    if not os.path.isfile(snapshot):
        with open(file, "rb") as src, open(snapshot, "wb") as dst:
            dst.write(src.read())
        return

    with open(snapshot, "r", errors="replace") as f:
        old_lines = f.readlines()
    with open(file, "r", errors="replace") as f:
        new_lines = f.readlines()

    sm = difflib.SequenceMatcher(a=old_lines, b=new_lines, autojunk=False)
    added_idx = [
        j
        for tag, _, _, j1, j2 in sm.get_opcodes()
        if tag in ("insert", "replace")
        for j in range(j1, j2)
    ]

    is_py = file.endswith(".py")
    in_any_string = triple_quote_state_per_line(new_lines) if is_py else None
    in_docstring = docstring_line_indices("".join(new_lines), len(new_lines)) if is_py else set()

    flagged = []
    for idx in added_idx:
        if idx == 0 and new_lines[idx].startswith("#!"):
            continue
        stripped = new_lines[idx].rstrip("\n")
        is_docstring_line = idx in in_docstring
        in_content_string_only = is_py and in_any_string[idx] and not is_docstring_line
        if in_content_string_only:
            continue
        if not (COMMENT_RE.match(stripped) or is_docstring_line):
            continue
        flagged.append(stripped.strip() or "(blank docstring line)")

    with open(snapshot, "w") as f:
        f.writelines(new_lines)

    if not flagged:
        return

    reason = (
        f"Touched {len(flagged)} comment/docstring line(s) in {os.path.basename(file)}. "
        "Don't render one verdict on the whole block below (keep it all / strip it all). "
        "Go line by line and cut only what actually violates global CLAUDE.md "
        "\"Comments and docstrings\": a task/ticket/issue reference (rots once it closes, "
        "belongs in the commit message), narration of what the code already shows, or "
        "anything over 15 lines with no non-obvious why. Leave the lines that state a "
        "real contract or a genuine why untouched.\n\nLines touched:\n" + "\n".join(flagged)
    )
    print(json.dumps({"decision": "block", "reason": reason}))


if __name__ == "__main__":
    main()
