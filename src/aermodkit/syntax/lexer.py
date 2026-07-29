"""Small lexer helpers for AERMOD free-format input lines."""

from __future__ import annotations

import shlex


def split_tokens(text: str) -> tuple[str, ...]:
    """Split a runstream line while respecting quoted filenames.

    The original line remains on the AST, so quote style and spacing are never
    lost in preserve mode.
    """

    lexer = shlex.shlex(text, posix=True)
    lexer.whitespace_split = True
    lexer.commenters = ""
    return tuple(lexer)


def classify_raw_line(text: str) -> str | None:
    stripped = text.lstrip()
    if not stripped:
        return "blank"
    if stripped.startswith("**") or stripped.startswith("!"):
        return "comment"
    return None
