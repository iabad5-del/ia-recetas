"""Streamlit UI entrypoint."""

from __future__ import annotations

import json
import logging
from typing import Any, Mapping

import streamlit as st

from config import AppConfig
from domain.recipe import Recipe
from exceptions import (
    InvalidLLMResponseError,
    LLMConfigurationError,
    LLMRequestError,
    ValidationError,
)
from llm.client import OpenRouterClient
from llm.mock_client import MockLLMClient
from llm.recipe_schema import (
    get_field_schema,
    is_field_hidden,
    iter_recipe_schema_fields,
)
from services.recipe_service import RecipeService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)


def build_recipe_service(use_mock: bool, temperature: float) -> RecipeService:
    """Create the recipe service with dependency injection."""
    if use_mock:
        return RecipeService(llm_client=MockLLMClient())

    config = AppConfig.from_env(temperature=temperature)
    client = OpenRouterClient(config=config)
    return RecipeService(llm_client=client)


def render_recipe(recipe: Recipe) -> None:
    """Render a validated recipe in the UI."""
    recipe_data = recipe.to_dict()

    with st.expander("Ver JSON de la receta", expanded=False):
        st.code(json.dumps(recipe_data, ensure_ascii=False, indent=2), language="json")

    rendered_fields: set[str] = set()
    for field_name in iter_recipe_schema_fields():
        if field_name not in recipe_data:
            continue
        _render_recipe_field(
            field_name=field_name,
            field_value=recipe_data[field_name],
            field_schema=get_field_schema(field_name),
        )
        rendered_fields.add(field_name)

    for field_name, field_value in recipe_data.items():
        if field_name in rendered_fields or is_field_hidden(field_name):
            continue
        _render_recipe_field(
            field_name=field_name,
            field_value=field_value,
            field_schema={},
        )


def _render_recipe_field(
    field_name: str,
    field_value: Any,
    field_schema: Mapping[str, Any],
) -> None:
    """Render a single recipe field based on schema metadata."""
    if is_field_hidden(field_name):
        return

    widget = field_schema.get("x-ui-widget")
    if widget == "title" and isinstance(field_value, str):
        st.subheader(field_value)
        return

    label = _field_label(field_name, field_schema)
    if isinstance(field_value, list):
        st.markdown(f"### {label}")
        list_style = field_schema.get("x-ui-list-style")
        for index, item in enumerate(field_value, start=1):
            if list_style == "numbered":
                st.write(f"{index}. {item}")
            else:
                st.write(f"- {item}")
        return

    st.write(f"{label}: {field_value}")


def _field_label(field_name: str, field_schema: Mapping[str, Any]) -> str:
    """Return a display label for a field."""
    schema_title = field_schema.get("title")
    if isinstance(schema_title, str) and schema_title.strip():
        return schema_title.strip()
    return field_name.replace("_", " ").capitalize()


def main() -> None:
    """Run Streamlit UI."""
    st.set_page_config(page_title="Generador de recetas", page_icon=":fork_and_knife:")
    st.title("Generador de recetas a partir de ingredientes")
    st.write(
        "Introduce los ingredientes que tienes disponibles para generar una receta. "
        "Puedes usar modo mock o una llamada real a OpenRouter."
    )

    ingredients = st.text_area(
        "Ingredientes disponibles",
        placeholder="Ejemplo: tomate, pasta, queso, aceite de oliva",
        height=120,
    )
    use_mock = st.checkbox(
        "Usar respuesta simulada (mock)",
        value=True,
        help="Si lo desactivas, la app usara OpenRouter y necesitara LLM_API_KEY.",
    )
    temperature = st.slider(
        "Temperatura del LLM",
        min_value=0.1,
        max_value=1.0,
        value=0.7,
        step=0.1,
        format="%.1f",
        help="Controla la creatividad de la respuesta: valores bajos son mas deterministas.",
    )

    if st.button("Generar receta"):
        try:
            service = build_recipe_service(use_mock=use_mock, temperature=temperature)
            with st.spinner("Generando receta..."):
                recipe = service.generate_recipe(ingredients)
        except ValidationError as exc:
            st.warning(str(exc))
            return
        except LLMConfigurationError as exc:
            st.error(str(exc))
            return
        except LLMRequestError as exc:
            st.error(str(exc))
            return
        except InvalidLLMResponseError as exc:
            st.error(str(exc))
            if exc.raw_response:
                with st.expander("Ver respuesta cruda del LLM", expanded=True):
                    st.code(exc.raw_response, language="text")
            return
        except Exception as exc:
            st.error(f"Error inesperado: {exc}")
            return

        render_recipe(recipe)


if __name__ == "__main__":
    main()
