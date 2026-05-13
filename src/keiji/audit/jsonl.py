"""Local JSONL audit writer for offline MVP testing."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class AuditEvent:
    """Single audit event."""

    event_type: str
    actor: str
    target_type: str
    target_id: str
    payload: dict[str, Any]
    created_at: str


def create_audit_event(
    *,
    event_type: str,
    actor: str,
    target_type: str,
    target_id: str,
    payload: dict[str, Any],
) -> AuditEvent:
    """Create an audit event with an UTC timestamp."""

    return AuditEvent(
        event_type=event_type,
        actor=actor,
        target_type=target_type,
        target_id=target_id,
        payload=payload,
        created_at=datetime.now(UTC).isoformat(),
    )


def append_audit_event(path: str | Path, event: AuditEvent) -> None:
    """Append a JSONL audit event to a local file."""

    audit_path = Path(path)
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    with audit_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(event), ensure_ascii=False, sort_keys=True) + "\n")
