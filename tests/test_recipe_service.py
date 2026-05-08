"""Tests for recipe service use case."""

from __future__ import annotations

from typing import Any

import pytest

from domain.recipe import Recipe
from exceptions import InvalidLLMResponseError, LLMRequestError, ValidationError
from services.recipe_service import RecipeService


class FakeSuccessClient:
    """Client double that returns a valid recipe payload."""

    def complete_json(self, prompt: str) -> dict[str, Any]:
        assert "tomate" in prompt
        return {
            "title": "Tostadas con tomate",
            "servings": 1,
            "ingredients": ["2 rebanadas de pan", "1 tomate maduro", "Aceite de oliva"],
            "time_minutes": 10,
            "difficulty": "Easy",
            "steps": [
                "Tuesta el pan.",
                "Ralla el tomate y mezclalo con aceite y sal.",
                "Reparte la mezcla sobre el pan tostado.",
            ],
        }


class FakeErrorClient:
    """Client double that raises a request error."""

    def complete_json(self, prompt: str) -> dict[str, Any]:
        _ = prompt
        raise LLMRequestError("network down")


class FakeInvalidPayloadClient:
    """Client double that returns an invalid type."""

    def complete_json(self, prompt: str) -> dict[str, Any]:
        _ = prompt
        return "invalid"  # type: ignore[return-value]


def test_recipe_service_generates_recipe() -> None:
    service = RecipeService(llm_client=FakeSuccessClient())

    recipe = service.generate_recipe("tomate, pan, aceite")

    assert isinstance(recipe, Recipe)
    assert recipe.title == "Tostadas con tomate"
    assert recipe.servings == 1


def test_recipe_service_rejects_empty_ingredients() -> None:
    service = RecipeService(llm_client=FakeSuccessClient())

    with pytest.raises(ValidationError):
        service.generate_recipe("   ")


def test_recipe_service_propagates_request_errors() -> None:
    service = RecipeService(llm_client=FakeErrorClient())

    with pytest.raises(LLMRequestError):
        service.generate_recipe("tomate")


def test_recipe_service_rejects_non_dict_payload() -> None:
    service = RecipeService(llm_client=FakeInvalidPayloadClient())

    with pytest.raises(InvalidLLMResponseError):
        service.generate_recipe("tomate")

