"""Prompt builders for recipe generation."""

from llm.recipe_schema import recipe_output_schema_as_text


def build_recipe_prompt(ingredients: str) -> str:
    """Build the prompt sent to the LLM from an ingredients list."""
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
