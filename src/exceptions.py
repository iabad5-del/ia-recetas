"""Custom exceptions for the recipe application."""


class RecipeAppError(Exception):
    """Base class for all app-specific exceptions."""


class LLMConfigurationError(RecipeAppError):
    """Raised when the LLM client configuration is invalid."""


class LLMRequestError(RecipeAppError):
    """Raised when the LLM request fails."""


class InvalidLLMResponseError(RecipeAppError):
    """Raised when the LLM returns an unexpected or invalid response."""


class ValidationError(RecipeAppError):
    """Raised when domain or input validation fails."""

