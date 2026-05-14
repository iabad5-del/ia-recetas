"""Recipe use-case service."""

from __future__ import annotations

from typing import Any, Callable, Protocol

from domain.recipe import Recipe
from exceptions import InvalidLLMResponseError, LLMRequestError, ValidationError
from llm.prompt_builder import build_recipe_prompt


class LLMClientProtocol(Protocol):
    """Protocol that any LLM client adapter must satisfy."""

    def complete_json(self, prompt: str) -> dict[str, Any]:
        """Return a JSON object produced from the prompt."""


class RecipeService:
    """Primary use case for recipe generation."""

    def __init__(
        self,
        llm_client: LLMClientProtocol,
        prompt_builder: Callable[[str], str] = build_recipe_prompt,
    ) -> None:
        self._llm_client = llm_client
        self._prompt_builder = prompt_builder

    def generate_recipe(self, ingredients: str) -> Recipe:
        """Generate a validated recipe from an ingredients input string."""
        cleaned_ingredients = self._validate_ingredients(ingredients)
        prompt = self._prompt_builder(cleaned_ingredients)
        raw_recipe = self._request_recipe(prompt)
        return Recipe.from_dict(raw_recipe)

    @staticmethod
    def _validate_ingredients(ingredients: str) -> str:
        if not isinstance(ingredients, str):
            raise ValidationError("ingredients must be a string.")

        cleaned_ingredients = ingredients.strip()
        if not cleaned_ingredients:
            raise ValidationError("ingredients cannot be empty.")
        return cleaned_ingredients

    def _request_recipe(self, prompt: str) -> dict[str, Any]:
        try:
            recipe_payload = self._llm_client.complete_json(prompt)
        except (LLMRequestError, InvalidLLMResponseError):
            raise
        except Exception as exc:
            raise LLMRequestError("Unexpected failure while requesting the LLM.") from exc

        if not isinstance(recipe_payload, dict):
            raise InvalidLLMResponseError("LLM client must return a JSON object.")
        return recipe_payload

