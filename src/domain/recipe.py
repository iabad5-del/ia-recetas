"""Recipe domain model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from exceptions import ValidationError

_ALLOWED_DIFFICULTIES = {"Easy", "Medium", "Hard"}


@dataclass(slots=True)
class Recipe:
    """Represents a generated cooking recipe."""

    title: str
    servings: int
    ingredients: list[str]
    time_minutes: int
    difficulty: str
    steps: list[str]
    chain_of_thought: str | None = None

    def __post_init__(self) -> None:
        """Validate and normalize recipe fields."""
        self.title = _validate_non_empty_string("title", self.title)
        self.servings = _validate_positive_int("servings", self.servings)
        self.ingredients = _validate_non_empty_string_list("ingredients", self.ingredients)
        self.time_minutes = _validate_positive_int("time_minutes", self.time_minutes)

        normalized_difficulty = _validate_non_empty_string("difficulty", self.difficulty).capitalize()
        if normalized_difficulty not in _ALLOWED_DIFFICULTIES:
            allowed = ", ".join(sorted(_ALLOWED_DIFFICULTIES))
            raise ValidationError(f"difficulty must be one of: {allowed}.")
        self.difficulty = normalized_difficulty

        self.steps = _validate_non_empty_string_list("steps", self.steps)
        if self.chain_of_thought is not None:
            self.chain_of_thought = _validate_non_empty_string(
                "chain_of_thought",
                self.chain_of_thought,
            )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Recipe":
        """Build a validated recipe from a raw dictionary."""
        required_fields = ("title", "servings", "ingredients", "time_minutes", "difficulty", "steps")
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            missing = ", ".join(missing_fields)
            raise ValidationError(f"Missing required recipe fields: {missing}.")

        return cls(
            title=data["title"],
            servings=data["servings"],
            ingredients=list(data["ingredients"]),
            time_minutes=data["time_minutes"],
            difficulty=data["difficulty"],
            steps=list(data["steps"]),
            chain_of_thought=data.get("chain_of_thought", data.get("chain_of_thougt")),
        )

    def to_dict(self) -> dict[str, Any]:
        """Export recipe as a JSON-serializable dictionary."""
        payload: dict[str, Any] = {}
        if self.chain_of_thought is not None:
            payload["chain_of_thought"] = self.chain_of_thought

        payload.update(
            {
                "title": self.title,
                "servings": self.servings,
                "ingredients": list(self.ingredients),
                "time_minutes": self.time_minutes,
                "difficulty": self.difficulty,
                "steps": list(self.steps),
            }
        )
        return payload


def _validate_non_empty_string(field_name: str, value: Any) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string.")

    cleaned = value.strip()
    if not cleaned:
        raise ValidationError(f"{field_name} cannot be empty.")
    return cleaned


def _validate_positive_int(field_name: str, value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"{field_name} must be an integer.")
    if value <= 0:
        raise ValidationError(f"{field_name} must be greater than 0.")
    return value


def _validate_non_empty_string_list(field_name: str, value: Any) -> list[str]:
    if not isinstance(value, list):
        raise ValidationError(f"{field_name} must be a list of strings.")
    if not value:
        raise ValidationError(f"{field_name} cannot be empty.")

    cleaned_items: list[str] = []
    for item in value:
        cleaned_items.append(_validate_non_empty_string(field_name, item))
    return cleaned_items
