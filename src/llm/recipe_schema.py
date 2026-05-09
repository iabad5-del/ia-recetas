"""Utilities for loading and querying recipe output schema."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

_SCHEMA_FILE = Path(__file__).resolve().with_name("recipe_output.schema.json")
_DEFAULT_HIDDEN_FIELDS = {"chain_of_thought", "chain_of_thougt"}


@lru_cache(maxsize=1)
def load_recipe_output_schema() -> dict[str, Any]:
    """Load the recipe JSON Schema from disk."""
    with _SCHEMA_FILE.open("r", encoding="utf-8") as schema_file:
        return json.load(schema_file)


def recipe_output_schema_as_text() -> str:
    """Return the recipe JSON Schema as pretty JSON text for prompt injection."""
    return json.dumps(load_recipe_output_schema(), ensure_ascii=False, indent=2)


def get_field_schema(field_name: str, schema: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Return the schema definition of a field, if available."""
    source = schema or load_recipe_output_schema()
    properties = source.get("properties")
    if not isinstance(properties, Mapping):
        return {}

    field_schema = properties.get(field_name)
    if not isinstance(field_schema, Mapping):
        return {}
    return dict(field_schema)


def is_field_hidden(field_name: str, schema: Mapping[str, Any] | None = None) -> bool:
    """Return True when a field should not be rendered in the UI."""
    field_schema = get_field_schema(field_name, schema)
    if field_schema.get("x-ui-hidden") is True:
        return True
    return field_name in _DEFAULT_HIDDEN_FIELDS


def iter_recipe_schema_fields(include_hidden: bool = False) -> list[str]:
    """Return schema fields preserving required-first order."""
    schema = load_recipe_output_schema()
    properties = schema.get("properties")
    if not isinstance(properties, Mapping):
        return []

    required = schema.get("required")
    required_fields = required if isinstance(required, list) else []

    ordered_fields: list[str] = []
    for field_name in required_fields:
        if field_name in properties and isinstance(field_name, str):
            ordered_fields.append(field_name)

    for field_name in properties.keys():
        if isinstance(field_name, str) and field_name not in ordered_fields:
            ordered_fields.append(field_name)

    if include_hidden:
        return ordered_fields
    return [field_name for field_name in ordered_fields if not is_field_hidden(field_name, schema)]
