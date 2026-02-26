from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class SessionState:
    messages: list[dict[str, str]] = field(default_factory=list)
    requirements: dict = field(default_factory=lambda: {
        "project_name": None,
        "app_type": None,
        "features": [],
        "target_users": None,
        "deployment_target": None,
    })


class SessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, SessionState] = {}

    def create(self) -> str:
        sid = str(uuid4())
        self._sessions[sid] = SessionState()
        return sid

    def get(self, session_id: str) -> SessionState:
        if session_id not in self._sessions:
            raise KeyError(f"Unknown session: {session_id}")
        return self._sessions[session_id]


store = SessionStore()
