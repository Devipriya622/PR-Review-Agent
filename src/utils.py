# src/utils.py
import re
import textwrap

def human_plural(n, singular, plural=None):
    if n == 1:
        return singular
    return plural or singular + "s"

def extract_language_from_filename(filename: str) -> str:
    lower = filename.lower()
    if lower.endswith(".py"):
        return "python"
    if lower.endswith(".js") or lower.endswith(".jsx") or lower.endswith(".ts"):
        return "javascript"
    if lower.endswith(".java"):
        return "java"
    if lower.endswith(".go"):
        return "go"
    if lower.endswith(".rb"):
        return "ruby"
    return "text"

def summarize_lines(lines, max_lines=5):
    if not lines:
        return ""
    if len(lines) <= max_lines:
        return "\n".join(lines)
    return "\n".join(lines[:max_lines]) + "\n... (truncated)"
