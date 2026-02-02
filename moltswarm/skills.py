"""Skill management system for MoltSwarm."""

from typing import Callable, Dict, List, Optional
from dataclasses import dataclass
from functools import wraps


@dataclass
class Skill:
    """Represents a skill that an AI agent can perform."""

    name: str
    handler: Callable
    description: str = ""
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class SkillRegistry:
    """Registry for managing agent skills."""

    def __init__(self):
        self._skills: Dict[str, Skill] = {}

    def register(self, name: str, description: str = "", tags: Optional[List[str]] = None):
        """Decorator to register a skill handler.

        Usage:
            @registry.register("code", description="Write code", tags=["#SKILL_CODE"])
            def handle_code(task):
                return result
        """
        def decorator(func: Callable) -> Callable:
            self._skills[name] = Skill(
                name=name,
                handler=func,
                description=description,
                tags=tags or [f"#SKILL_{name.upper()}"]
            )
            return func
        return decorator

    def get(self, name: str) -> Optional[Skill]:
        """Get a skill by name."""
        return self._skills.get(name)

    def get_all(self) -> Dict[str, Skill]:
        """Get all registered skills."""
        return self._skills.copy()

    def get_tags(self) -> List[str]:
        """Get all skill tags."""
        tags = []
        for skill in self._skills.values():
            tags.extend(skill.tags)
        return list(set(tags))

    def can_handle(self, task_skills: List[str]) -> bool:
        """Check if registry can handle a task with required skills."""
        my_tags = self.get_tags()
        my_tags_normalized = [t.lstrip("#").lower() for t in my_tags]
        task_normalized = [t.lstrip("#").lower() for t in task_skills]

        return any(req in my_tags_normalized for req in task_normalized)

    def find_handler(self, task_skills: List[str]) -> Optional[Callable]:
        """Find the best handler for a task based on skills."""
        for skill_name, skill in self._skills.items():
            for tag in skill.tags:
                tag_normalized = tag.lstrip("#").lower()
                if any(tag_normalized in t.lstrip("#").lower() for t in task_skills):
                    return skill.handler
        return None
