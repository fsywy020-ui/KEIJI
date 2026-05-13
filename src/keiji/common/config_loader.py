"""Dependency-free configuration loader for KEIJI YAML rule files.

The runtime environment intentionally avoids external dependencies for the
initial offline MVP. This parser supports the YAML subset used by the versioned
rule files in ``config/``: nested mappings, lists, strings, booleans, integers,
floats, and quoted scalars.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def load_rule_config(path: str | Path) -> dict[str, Any]:
    """Load a KEIJI YAML rule file without network or third-party packages."""

    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(config_path)
    parsed = _parse_yaml_subset(config_path.read_text(encoding="utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError(f"expected mapping at top level: {config_path}")
    return parsed


def _parse_yaml_subset(text: str) -> Any:
    lines = [line.rstrip("\n") for line in text.splitlines()]
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]

    for index, raw_line in enumerate(lines):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if line.startswith("- "):
            if not isinstance(parent, list):
                raise ValueError(f"list item without list parent: {raw_line}")
            item_text = line[2:].strip()
            if ":" in item_text and not item_text.startswith(('"', "'")):
                key, value_text = item_text.split(":", 1)
                item: dict[str, Any] = {key.strip(): _parse_scalar(value_text.strip())}
                parent.append(item)
                stack.append((indent, item))
            else:
                parent.append(_parse_scalar(item_text))
            continue

        if ":" not in line:
            raise ValueError(f"unsupported YAML line: {raw_line}")

        key, value_text = line.split(":", 1)
        key = key.strip()
        value_text = value_text.strip()
        if not isinstance(parent, dict):
            raise ValueError(f"mapping entry without mapping parent: {raw_line}")

        if value_text:
            parent[key] = _parse_scalar(value_text)
            continue

        child = _next_container(lines, index, indent)
        parent[key] = child
        stack.append((indent, child))

    return root


def _next_container(lines: list[str], current_index: int, current_indent: int) -> dict[str, Any] | list[Any]:
    for next_line in lines[current_index + 1 :]:
        if not next_line.strip() or next_line.lstrip().startswith("#"):
            continue
        next_indent = len(next_line) - len(next_line.lstrip(" "))
        if next_indent <= current_indent:
            return {}
        return [] if next_line.strip().startswith("- ") else {}
    return {}


def _parse_scalar(value: str) -> Any:
    if value == "":
        return ""
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "None", "~"}:
        return None
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value
