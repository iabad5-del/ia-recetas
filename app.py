import streamlit as st
import json

def call_llm_mock(prompt: str) -> dict:
    """
    Aquesta funció simula la resposta d'un LLM.
    Rep un prompt (text) i retorna un diccionari amb una recepta.
    Més endavant, aquí dins és on farem la crida real a l'API del LLM.
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
        "difficulty": "Fàcil",
        "steps": [
            "Bull la pasta en una olla amb aigua i sal fins que sigui al punt.",
            "Mentrestant, talla els tomàquets a dauets i salta'ls en una paella amb oli d'oliva.",
            "Salpebra la salsa de tomàquet i barreja-la amb la pasta escorreguda.",
            "Serveix al plat i afegeix el formatge ratllat per sobre."
        ]
    }
    return recipe

st.title("Generador de receptes")

ingredients = st.text_area(
    "Escriu aquí els ingredients que tens disponibles:",
    placeholder="Exemple: tomàquet, pasta, formatge, oli d'oliva"
)

if st.button("Generar recepta (mock)"):
    if ingredients.strip() == "":
        st.warning("No has escrit cap ingredient.")
    else:
        # Aquí construïm el prompt que, en el futur, enviarem al LLM
        prompt = f"Genera una recepta en format JSON amb títol, racions, ingredients, temps aproximat, nivell de dificultat i passos, utilitzant aquests ingredients: {ingredients}"

        # Cridem la funció mock (més endavant serà una crida real al LLM)
        recipe = call_llm_mock(prompt)

        # Opcional: veure la recepta com a JSON (com si fos la resposta del LLM)
        recipe_json = json.dumps(recipe, ensure_ascii=False, indent=2)
        st.markdown("### JSON de la recepta (simulació de resposta d'un LLM)")
        st.code(recipe_json, language="json")

        # Mostrar la recepta parsejada
        st.subheader(recipe["title"])
        st.write(f"Racions: {recipe['servings']}")
        st.write(f"Temps aproximat: {recipe['time_minutes']} minuts")
        st.write(f"Nivell de dificultat: {recipe['difficulty']}")

        st.markdown("### Ingredients")
        for item in recipe["ingredients"]:
            st.write(f"- {item}")

        st.markdown("### Passos")
        for i, step in enumerate(recipe["steps"], start=1):
            st.write(f"{i}. {step}")
