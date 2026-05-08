"""Tests for recipe prompt builder."""

from llm.prompt_builder import build_recipe_prompt


def test_build_recipe_prompt_includes_ingredients_and_json_instruction() -> None:
    ingredients = "tomate, pasta, queso"

    prompt = build_recipe_prompt(ingredients)

    assert ingredients in prompt
    assert "Answer ONLY with the JSON object." in prompt
    assert '"title": "string, short and descriptive name of the recipe"' in prompt

