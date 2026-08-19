"""NewDB SDK Exceptions."""


class NewDBError(Exception):
    """Base exception for all NewDB SDK errors."""
    pass


class AuthenticationError(NewDBError):
    """Raised when the API key is missing or invalid."""
    pass


class RateLimitError(NewDBError):
    """Raised when the API rate limit or concurrency limit is reached."""
    pass


class ValidationError(NewDBError):
    """Raised when request parameters fail schema validation."""
    pass


class TimeoutError(NewDBError):
    """Raised when polling for a task result times out."""
    pass


class APIResponseError(NewDBError):
    """Raised when NewDB API returns an HTTP or server error."""
    def __init__(self, message: str, status_code: int = 500, response_data: dict = None):
        super().__init__(f"[{status_code}] {message}")
        self.status_code = status_code
        self.response_data = response_data or {}
