"""Tests for mock LLM client."""

from domain.recipe import Recipe
from llm.mock_client import MockLLMClient


def test_mock_client_returns_valid_recipe_payload() -> None:
    client = MockLLMClient()

    payload = client.complete_json("any prompt")
    recipe = Recipe.from_dict(payload)

    assert recipe.title
    assert recipe.servings > 0
    assert len(recipe.ingredients) > 0
    assert len(recipe.steps) > 0

