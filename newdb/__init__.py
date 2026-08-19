"""Official Python SDK for NewDB REST API."""

from .client import NewDBClient, AsyncNewDBClient
from .models import BalanceResponse, MethodResult, TaskResponse
from .exceptions import (
    NewDBError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    TimeoutError,
    APIResponseError,
)

__version__ = "1.0.0"
__all__ = [
    "NewDBClient",
    "AsyncNewDBClient",
    "BalanceResponse",
    "MethodResult",
    "TaskResponse",
    "NewDBError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "TimeoutError",
    "APIResponseError",
]
