# Recipe App (Clean Architecture + Streamlit)

Aplicacion de generacion de recetas con Streamlit y un cliente LLM OpenAI-compatible (OpenRouter), refactorizada con separacion estricta de responsabilidades.

## Arquitectura

```text
recipe_app/
│
├── app.py
├── config.py
├── domain/
│   └── recipe.py
├── services/
│   └── recipe_service.py
├── llm/
│   ├── prompt_builder.py
│   ├── client.py
│   └── mock_client.py
└── exceptions.py
```

Responsabilidades:

- `recipe_app/app.py`: solo UI Streamlit (inputs, spinner, outputs, errores).
- `recipe_app/config.py`: configuracion centralizada via entorno.
- `recipe_app/domain/recipe.py`: modelo de dominio `Recipe` con validaciones.
- `recipe_app/services/recipe_service.py`: caso de uso principal.
- `recipe_app/llm/prompt_builder.py`: construccion de prompts.
- `recipe_app/llm/client.py`: adaptador HTTP real para OpenRouter.
- `recipe_app/llm/mock_client.py`: adaptador mock con misma interfaz.
- `recipe_app/exceptions.py`: errores custom de la aplicacion.

## Requisitos

- Python 3.11+

## Instalacion

```bash
pip install -r requirements.txt
```

## Configuracion

Variables de entorno soportadas:

- `LLM_API_KEY` (obligatoria solo en modo real)
- `LLM_API_URL` (default: `https://openrouter.ai/api/v1/chat/completions`)
- `LLM_MODEL` (default: `openrouter/auto`)
- `LLM_TIMEOUT_SECONDS` (default: `30`)
- `LLM_MAX_TOKENS` (default: `600`)

Ejemplo PowerShell:

```powershell
$env:LLM_API_KEY="tu_api_key"
$env:LLM_MODEL="openrouter/auto"
```

## Ejecucion

```bash
streamlit run recipe_app/app.py
```

## Modo mock

La UI incluye el checkbox **"Usar respuesta simulada (mock)"**:

- Activado: usa `MockLLMClient`, no necesita `LLM_API_KEY`.
- Desactivado: usa `OpenRouterClient`, requiere `LLM_API_KEY`.

## Tests

```bash
pytest -q
```

Incluye tests unitarios para:

- `RecipeService`
- Prompt builder
- Mock client
