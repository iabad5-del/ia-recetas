"""Prompt builders for recipe generation."""


def build_recipe_prompt(ingredients: str) -> str:
    """Build the recipe-generation prompt from user ingredients."""
    return f"""
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
""".strip()

