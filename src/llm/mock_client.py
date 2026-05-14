"""Mock LLM client for local development and testing."""

from __future__ import annotations

from typing import Any


class MockLLMClient:
    """Mock implementation of the LLM client interface."""

    def complete_json(self, prompt: str) -> dict[str, Any]:
        """Return a deterministic valid recipe payload."""
        _ = prompt
        return {
            "chain_of_thought": (
                "1. Analizo ingredientes base. 2. Elijo una receta simple con tomate y pasta. "
                "3. Propongo tecnica rapida para principiantes."
            ),
            "title": "Pasta con salsa de tomate rapida",
            "servings": 2,
            "ingredients": [
                "200 g de pasta",
                "2 tomates maduros",
                "2 cucharadas de aceite de oliva",
                "50 g de queso rallado",
                "Sal y pimienta al gusto",
            ],
            "time_minutes": 20,
            "difficulty": "Easy",
            "steps": [
                "Hierve la pasta en agua con sal hasta que quede al dente.",
                "Sofrie los tomates picados con aceite de oliva durante 8 minutos.",
                "Mezcla la pasta escurrida con la salsa de tomate y ajusta sal y pimienta.",
                "Sirve caliente con queso rallado por encima.",
            ],
        }
