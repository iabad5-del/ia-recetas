import streamlit as st
import json
import requests
import os

st.set_page_config(page_title="Generador de receptes", page_icon="🍽️")


# ------------------- PROMPT ENGINEERING -------------------

def build_prompt(ingredients: str) -> str:
    """
    Construeix el prompt que enviarem al LLM a partir dels ingredients.
    """
    prompt = f"""
You are a professional chef AI.

Your task is to create ONE cooking recipe using mainly the following available ingredients:
{ingredients}

Return the recipe STRICTLY as a single JSON object with this exact structure:

{{
  "title": "string, short and descriptive name of the recipe",
  "servings": integer,
  "ingredients": [
    "string with quantity and ingredient, e.g. '200 g pasta'",
    "string ...",
    "... "
  ],
  "time_minutes": integer,
  "difficulty": "string, one of: 'Easy', 'Medium', 'Hard'",
  "steps": [
    "string describing step 1",
    "string describing step 2",
    "string describing step 3",
    "... "
  ]
}}

Rules:
- Use mostly the ingredients provided, you can add a few basic pantry items if needed (salt, oil, etc.).
- Make sure the JSON is valid and can be parsed by a JSON parser.
- Do NOT include any text before or after the JSON.
- Do NOT include comments in the JSON.
- Answer ONLY with the JSON object.
"""
    return prompt


# ------------------- MOCK (SIMULACIÓ) -------------------

def call_llm_mock(prompt: str) -> dict:
    """
    Simula la resposta d'un LLM.
    Retorna sempre la mateixa recepta, amb el format objectiu.
    """
    recipe = {
        "title": "Pasta amb salsa de tomàquet ràpida",
        "servings": 2,
        "ingredients": [
            "200 g de pasta seca",
            "2 tomàquets madurs",
            "50 g de formatge ratllat",
            "2 cullerades d'oli d'oliva",
            "Sal i pebre al gust"
        ],
        "time_minutes": 20,
        "difficulty": "Easy",
        "steps": [
            "Bull la pasta en una olla amb aigua i sal fins que sigui al punt.",
            "Mentrestant, talla els tomàquets a dauets i salta'ls en una paella amb oli d'oliva.",
            "Salpebra la salsa de tomàquet i barreja-la amb la pasta escorreguda.",
            "Serveix al plat i afegeix el formatge ratllat per sobre."
        ]
    }
    return recipe


# ------------------- CRIDA REAL AL LLM (ESQUELET) -------------------

def call_llm_real(prompt: str) -> dict:
    """
    Crida real a un model LLM via una API OpenAI-compatible (per exemple GPTFree o similar).
    - Assumeix un endpoint tipus /v1/chat/completions.
    - Rep un prompt (text) i retorna un diccionari Python amb la recepta.
    """

    # 1. Configuració bàsica de l'API
    # TODO: canvieu aquesta URL per la URL del vostre proveïdor
    api_url = "https://API_BASE_URL/v1/chat/completions"

    # API key del proveïdor (millor com a variable d'entorn)
    api_key = os.environ.get("LLM_API_KEY", "")
    if not api_key:
        raise RuntimeError(
            "No s'ha trobat la variable d'entorn LLM_API_KEY. "
            "Definiu-la amb la vostra API key del proveïdor."
        )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # 2. Cos de la petició (format OpenAI-style)
    payload = {
        # TODO: canvieu el nom del model pel que indiqui el vostre proveïdor
        "model": "NOM_DEL_MODEL",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 600,
        "temperature": 0.7,
    }

    # 3. Petició HTTP
    response = requests.post(api_url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()

    # 4. Extreure el text de la resposta
    # Format típic OpenAI-like: choices[0].message.content
    try:
        content = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Resposta inesperada del LLM: {result}") from e

    # 5. Convertir el text (que hauria de ser JSON) a diccionari Python
    try:
        recipe = json.loads(content)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"El model ha retornat un text que no és JSON vàlid:\n{content}"
        ) from e

    return recipe


# ------------------- FUNCIÓ PUNT D'ENTRADA LLM -------------------

def call_llm(prompt: str, use_mock: bool = True) -> dict:
    """
    Punt únic d'entrada per obtenir una recepta.
    - Si use_mock és True, usa la recepta simulada.
    - Si use_mock és False, fa la crida real a l'API del LLM.
    """
    if use_mock:
        return call_llm_mock(prompt)
    return call_llm_real(prompt)


# ------------------- INTERFÍCIE STREAMLIT -------------------

st.title("Generador de receptes a partir d'ingredients")

st.write(
    "Introdueix els ingredients que tens disponibles i genera una recepta. "
    "Ara mateix pots fer servir una resposta simulada (mock) o, quan estigui configurada, "
    "una crida real a un model de llenguatge (LLM)."
)

ingredients = st.text_area(
    "Escriu aquí els ingredients que tens disponibles:",
    placeholder="Exemple: tomàquet, pasta, formatge, oli d'oliva",
    height=120,
)

use_mock = st.checkbox(
    "Fer servir resposta simulada (mock)",
    value=True,
    help="Quan desactiveu aquesta opció i estigui configurada l'API, "
         "l'app consultarà el LLM de veritat."
)

if st.button("Generar recepta"):
    if ingredients.strip() == "":
        st.warning("No has escrit cap ingredient.")
    else:
        with st.spinner("Generant recepta..."):
            prompt = build_prompt(ingredients)

            try:
                recipe = call_llm(prompt, use_mock=use_mock)
            except RuntimeError as e:
                st.error(str(e))
                st.stop()
            except json.JSONDecodeError:
                st.error(
                    "La resposta del LLM no és un JSON vàlid. "
                    "Reviseu el prompt i el format de sortida."
                )
                st.stop()
            except Exception as e:
                st.error(f"S'ha produït un error en consultar el model: {e}")
                st.stop()

        # Mostrem el JSON de la recepta (per transparència i depuració)
        recipe_json = json.dumps(recipe, ensure_ascii=False, indent=2)
        st.markdown("### JSON de la recepta")
        st.code(recipe_json, language="json")

        # Mostrar la recepta parsejada
        st.subheader(recipe.get("title", "Recepta sense títol"))
        st.write(f"Racions: {recipe.get('servings', 'N/A')}")
        st.write(f"Temps aproximat: {recipe.get('time_minutes', 'N/A')} minuts")
        st.write(f"Nivell de dificultat: {recipe.get('difficulty', 'N/A')}")

        st.markdown("### Ingredients")
        for item in recipe.get("ingredients", []):
            st.write(f"- {item}")

        st.markdown("### Passos")
        for i, step in enumerate(recipe.get("steps", []), start=1):
            st.write(f"{i}. {step}")
