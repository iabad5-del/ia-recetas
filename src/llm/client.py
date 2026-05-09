"""OpenRouter client adapter."""

from __future__ import annotations

import json
import logging
from typing import Any

import requests

from config import AppConfig
from exceptions import (
    InvalidLLMResponseError,
    LLMConfigurationError,
    LLMRequestError,
)

logger = logging.getLogger(__name__)


class OpenRouterClient:
    """HTTP client for OpenAI-compatible providers such as OpenRouter."""

    def __init__(self, config: AppConfig, session: requests.Session | None = None) -> None:
        if not config.api_key:
            raise LLMConfigurationError(
                "LLM_API_KEY is missing. Configure it before using the real LLM client."
            )
        self._config = config
        self._session = session or requests.Session()

    def complete_json(self, prompt: str) -> dict[str, Any]:
        """
        Send a completion request and return a parsed JSON object.

        The provider response is expected to follow the OpenAI-compatible
        chat completion schema and to contain a JSON object in `message.content`.
        """
        payload = {
            "model": self._config.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": self._config.max_tokens,
            "temperature": self._config.temperature,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._config.api_key}",
        }

        try:
            response = self._session.post(
                self._config.api_url,
                headers=headers,
                json=payload,
                timeout=self._config.timeout_seconds,
            )
            response.raise_for_status()
        except requests.Timeout as exc:
            raise LLMRequestError("LLM request timed out.") from exc
        except requests.HTTPError as exc:
            status_code = exc.response.status_code if exc.response is not None else "unknown"
            raise LLMRequestError(f"LLM request failed with HTTP status {status_code}.") from exc
        except requests.RequestException as exc:
            raise LLMRequestError("LLM request failed due to a network error.") from exc

        try:
            provider_response = response.json()
        except ValueError as exc:
            raise InvalidLLMResponseError(
                "Provider returned non-JSON response payload.",
                raw_response=response.text,
            ) from exc

        content = self._extract_content(provider_response)
        logger.info("LLM raw response content: %s", content)

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            raise InvalidLLMResponseError(
                "LLM content is not valid JSON.",
                raw_response=content,
            ) from exc

        if not isinstance(parsed, dict):
            raise InvalidLLMResponseError(
                "LLM JSON response must be an object.",
                raw_response=content,
            )
        return parsed

    @staticmethod
    def _extract_content(provider_response: Any) -> str:
        if not isinstance(provider_response, dict):
            raise InvalidLLMResponseError("Unexpected provider response type.")

        try:
            content = provider_response["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise InvalidLLMResponseError("Unexpected provider response structure.") from exc

        if not isinstance(content, str) or not content.strip():
            raise InvalidLLMResponseError("Provider returned empty completion content.")

        return content
