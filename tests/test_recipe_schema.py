"""Tests for recipe output schema utilities."""

from llm.recipe_schema import (
    is_field_hidden,
    iter_recipe_schema_fields,
    load_recipe_output_schema,
    recipe_output_schema_as_text,
)


def test_load_recipe_output_schema_contains_core_fields() -> None:
    schema = load_recipe_output_schema()

    assert "properties" in schema
    properties = schema["properties"]
    assert "title" in properties
    assert "ingredients" in properties


def test_iter_recipe_schema_fields_excludes_hidden_fields() -> None:
    fields = iter_recipe_schema_fields()

    assert "chain_of_thought" not in fields
    assert "title" in fields
    assert "steps" in fields


def test_is_field_hidden_supports_chain_of_thought_typos() -> None:
    assert is_field_hidden("chain_of_thought")
    assert is_field_hidden("chain_of_thougt")


def test_recipe_output_schema_as_text_contains_json_schema_uri() -> None:
    schema_text = recipe_output_schema_as_text()

    assert '"$schema": "https://json-schema.org/draft/2020-12/schema"' in schema_text
