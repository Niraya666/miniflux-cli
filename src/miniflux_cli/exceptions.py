"""CLI-specific exceptions with stable exit codes."""


class CLIError(Exception):
    """Base exception with a default exit code of 1."""

    exit_code: int = 1

    def __init__(self, message: str, exit_code: int | None = None) -> None:
        super().__init__(message)
        if exit_code is not None:
            self.exit_code = exit_code


class BadRequestError(CLIError):
    """Invalid arguments or bad request from the API."""

    exit_code: int = 2


class AuthError(CLIError):
    """Authentication or authorization failure."""

    exit_code: int = 3


class NotFoundError(CLIError):
    """Requested resource was not found."""

    exit_code: int = 4


class ServerError(CLIError):
    """Server-side error (5xx)."""

    exit_code: int = 5
