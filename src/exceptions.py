"""Custom exceptions for the recipe application."""


class RecipeAppError(Exception):
    """Base class for all app-specific exceptions."""


class LLMConfigurationError(RecipeAppError):
    """Raised when the LLM client configuration is invalid."""


class LLMRequestError(RecipeAppError):
    """Raised when the LLM request fails."""


class InvalidLLMResponseError(RecipeAppError):
    """Raised when the LLM returns an unexpected or invalid response."""

    def __init__(self, message: str, *, raw_response: str | None = None) -> None:
        super().__init__(message)
        self.raw_response = raw_response


class ValidationError(RecipeAppError):
    """Raised when domain or input validation fails."""
