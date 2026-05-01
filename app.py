import streamlit as st

st.title("Generador de receptes")

ingredients = st.text_area(
    "Escriu aquí els ingredients que tens disponibles:",
    placeholder="Exemple: tomàquet, pasta, formatge, oli d'oliva"
)

if st.button("Mostrar ingredients"):
    if ingredients.strip() == "":
        st.warning("No has escrit cap ingredient.")
    else:
        st.subheader("Ingredients introduïts")
        st.write(ingredients)
