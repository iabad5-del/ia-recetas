"""Streamlit UI entrypoint."""

from __future__ import annotations

import json
import logging

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
    with st.expander("Ver JSON de la receta", expanded=False):
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
