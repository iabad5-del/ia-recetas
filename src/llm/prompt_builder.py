"""Prompt builders for recipe generation."""

from llm.recipe_schema import recipe_output_schema_as_text


def build_recipe_prompt(ingredients: str) -> str:
    """
    JUSTIFICACIÓ DE LES TÈCNIQUES DE PROMPT ENGINEERING APLICADES:
    Aquest prompt ha estat dissenyat per maximitzar la qualitat culinària i garantir
    l'estabilitat del parseig de dades en el backend, aplicant aquestes tècniques:

    1. Etiquetatge (XML Tags): L'ús d'etiquetes (<role>, <instructions>, etc.) estructura 
       clarament les parts del prompt. Això ajuda el model a distingir ràpidament el 
       context de les instruccions i les regles estrictes.
       
    2. Role-playing, To i Audiència (<role>): S'assigna una personalitat experta 
       ("professional chef AI"), un to ("enthusiastic") i una audiència clara 
       ("beginner cooks"). Això assegura que la resposta tingui un vocabulari 
       adequat, pedagògic i amb molt de sentit culinari.
       
    3. Descripció Clara i Concisa (<instructions>): S'especifica exactament què ha de 
       fer la IA ("create ONE cooking recipe"), evitant ambigüitats i forçant-la a 
       treballar estrictament amb els ingredients de l'usuari.
       
    4. Cadena de Pensament / Chain of Thought (CoT): S'instrueix el model a raonar 
       pas a pas abans de donar la recepta (analitzar, pensar el perfil de sabors i 
       planificar). Aquest procés s'encapsula com a primer camp dins de l'esquema 
       JSON ("chain_of_thought") per obligar la IA a reflexionar i millorar la 
       qualitat de la recepta, sense trencar el format de dades.
       
    5. Sortida Estructurada (<json_schema>): S'imposa un contracte de dades rígid. 
       És indispensable per garantir la interoperabilitat i poder mapejar els valors 
       en diferents components de Streamlit, complint la norma del Repte 7 de no 
       mostrar el text en brut.
       
    6. Single-shot Prompting (<example>): Es proporciona un exemple complet d'un 
       JSON vàlid. Mostrar a la IA una demostració d'allò que s'espera redueix 
       dràsticament la probabilitat que s'equivoqui en el format (com ara llistes 
       d'ingredients o de passos).
       
    7. Negative Prompting i Restriccions (<rules>): S'indica de forma explícita què 
       TÉ PROHIBIT fer ("Do NOT include any text before or after..."). Actua com a 
       salvaguarda fonamental per evitar al·lucinacions conversacionals prèvies 
       (ex. "Aquí tens la teva recepta!") que trencarien la funció `json.loads()`.
    ---------------------------------------------------------------------------
    
    """
    recipe_schema = recipe_output_schema_as_text()
    return f"""<role>
You are a professional chef AI. Your tone is enthusiastic and encouraging.
Your audience are beginner cooks who need simple, easy-to-follow explanations.
</role>

<instructions>
Your task is to create ONE cooking recipe using mainly the following available ingredients:
{ingredients}

Before creating the recipe, think step-by-step about flavor profiles, ingredient combinations, and the cooking method.
</instructions>

<json_schema>
Return the recipe STRICTLY as a single JSON object that validates against this JSON Schema:
{recipe_schema}
</json_schema>

<rules>
- Use mostly the ingredients provided, you can add a few basic pantry items if needed (salt, oil, etc.).
- Make sure the JSON is valid and can be parsed by a JSON parser.
- Do NOT include any text before or after the JSON.
- Do NOT include comments in the JSON.
- Answer ONLY with the JSON object.
</rules>"""
