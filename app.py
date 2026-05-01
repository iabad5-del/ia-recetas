import streamlit as st

st.title("Generador de receptes")

ingredients = st.text_area(
    "Escriu aquí els ingredients que tens disponibles:",
    placeholder="Exemple: tomàquet, pasta, formatge, oli d'oliva"
)

if st.button("Generar recepta (mock)"):
    if ingredients.strip() == "":
        st.warning("No has escrit cap ingredient.")
    else:
        # Recepta simulada (mock), més endavant vindrà d'un LLM
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
