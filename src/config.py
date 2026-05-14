"""Application configuration for LLM access and generation parameters."""

from __future__ import annotations

import os
from dataclasses import dataclass

from exceptions import LLMConfigurationError


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Centralized runtime configuration for the app."""

    api_url: str
    api_key: str
    model: str
    timeout_seconds: float
    max_tokens: int
    temperature: float

    @classmethod
    def from_env(cls, *, temperature: float = 0.7) -> "AppConfig":
        """Build configuration from environment variables and runtime parameters."""
        api_url = os.getenv("LLM_API_URL", "https://openrouter.ai/api/v1/chat/completions").strip()
        api_key = os.getenv("LLM_API_KEY", "").strip()
        model = os.getenv("LLM_MODEL", "openrouter/auto").strip()
        timeout_seconds = _parse_float("LLM_TIMEOUT_SECONDS", default=30.0, min_value=0.1)
        max_tokens = _parse_int("LLM_MAX_TOKENS", default=600, min_value=1)
        resolved_temperature = _validate_float("temperature", temperature, min_value=0.0, max_value=1.0)

        if not api_url:
            raise LLMConfigurationError("LLM_API_URL cannot be empty.")
        if not model:
            raise LLMConfigurationError("LLM_MODEL cannot be empty.")

        return cls(
            api_url=api_url,
            api_key=api_key,
            model=model,
            timeout_seconds=timeout_seconds,
            max_tokens=max_tokens,
            temperature=resolved_temperature,
        )


def _parse_int(name: str, *, default: int, min_value: int | None = None) -> int:
    raw_value = os.getenv(name, str(default)).strip()
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise LLMConfigurationError(f"{name} must be an integer. Received: {raw_value!r}") from exc

    if min_value is not None and value < min_value:
        raise LLMConfigurationError(f"{name} must be >= {min_value}. Received: {value}")
    return value


def _parse_float(
    name: str,
    *,
    default: float,
    min_value: float | None = None,
    max_value: float | None = None,
) -> float:
    raw_value = os.getenv(name, str(default)).strip()
    try:
        value = float(raw_value)
    except ValueError as exc:
        raise LLMConfigurationError(f"{name} must be a number. Received: {raw_value!r}") from exc

    if min_value is not None and value < min_value:
        raise LLMConfigurationError(f"{name} must be >= {min_value}. Received: {value}")
    if max_value is not None and value > max_value:
        raise LLMConfigurationError(f"{name} must be <= {max_value}. Received: {value}")
    return value


def _validate_float(
    name: str,
    value: float,
    *,
    min_value: float | None = None,
    max_value: float | None = None,
) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise LLMConfigurationError(f"{name} must be a number. Received: {value!r}")

    numeric_value = float(value)
    if min_value is not None and numeric_value < min_value:
        raise LLMConfigurationError(f"{name} must be >= {min_value}. Received: {numeric_value}")
    if max_value is not None and numeric_value > max_value:
        raise LLMConfigurationError(f"{name} must be <= {max_value}. Received: {numeric_value}")
    return numeric_value
