"""Tests for application configuration."""

from __future__ import annotations

import pytest

from config import AppConfig
from exceptions import LLMConfigurationError


def test_from_env_allows_temperature_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_TEMPERATURE", "0.1")

    config = AppConfig.from_env(temperature=0.4)

    assert config.temperature == 0.4


def test_from_env_rejects_invalid_temperature_override() -> None:
    with pytest.raises(LLMConfigurationError):
        AppConfig.from_env(temperature=1.5)


def test_from_env_uses_default_temperature_when_not_provided(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LLM_TEMPERATURE", "0.1")

    config = AppConfig.from_env()

    assert config.temperature == 0.7
