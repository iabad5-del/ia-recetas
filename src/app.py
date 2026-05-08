"""Streamlit UI entrypoint."""

from __future__ import annotations

import json

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
from services.recipe_service import RecipeService


def build_recipe_service(use_mock: bool) -> RecipeService:
    """Create the recipe service with dependency injection."""
    if use_mock:
        return RecipeService(llm_client=MockLLMClient())

    config = AppConfig.from_env()
    client = OpenRouterClient(config=config)
    return RecipeService(llm_client=client)


def render_recipe(recipe: Recipe) -> None:
    """Render a validated recipe in the UI."""
    st.markdown("### JSON de la receta")
    st.code(json.dumps(recipe.to_dict(), ensure_ascii=False, indent=2), language="json")

    st.subheader(recipe.title)
    st.write(f"Raciones: {recipe.servings}")
    st.write(f"Tiempo aproximado: {recipe.time_minutes} minutos")
    st.write(f"Dificultad: {recipe.difficulty}")

    st.markdown("### Ingredientes")
    for ingredient in recipe.ingredients:
        st.write(f"- {ingredient}")

    st.markdown("### Pasos")
    for index, step in enumerate(recipe.steps, start=1):
        st.write(f"{index}. {step}")


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

    if st.button("Generar receta"):
        try:
            service = build_recipe_service(use_mock=use_mock)
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
            return
        except Exception as exc:
            st.error(f"Error inesperado: {exc}")
            return

        render_recipe(recipe)


if __name__ == "__main__":
    main()

