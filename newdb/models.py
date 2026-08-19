"""Data models and response helpers for NewDB SDK."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class BalanceResponse:
    token: str
    balance: int
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MethodResult:
    status: int
    data: Any = None
    error: Optional[str] = None
    found: Optional[bool] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskResponse:
    request_id: str
    state: str  # "queued", "in progress", "complete", "failed", "restart"
    results: Dict[str, MethodResult] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_complete(self) -> bool:
        return self.state.lower() == "complete"

    @property
    def is_failed(self) -> bool:
        return self.state.lower() in {"failed", "error"}

    @property
    def is_in_progress(self) -> bool:
        return self.state.lower() in {"queued", "in progress", "restart", "in_progress"}

    def get_result(self, method: str) -> Optional[MethodResult]:
        return self.results.get(method)
