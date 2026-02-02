"""Tests for MoltSwarm skills registry."""

from moltswarm.skills import SkillRegistry


def test_register_skill():
    """Test registering a skill."""
    registry = SkillRegistry()

    @registry.register("code", description="Write code", tags=["#SKILL_CODE"])
    def handle_code(task):
        return "code"

    skill = registry.get("code")
    assert skill is not None
    assert skill.name == "code"
    assert skill.description == "Write code"
    assert "#SKILL_CODE" in skill.tags


def test_get_tags():
    """Test getting all skill tags."""
    registry = SkillRegistry()

    @registry.register("code", tags=["#SKILL_CODE"])
    def handle_code(task):
        return "code"

    @registry.register("write", tags=["#SKILL_WRITE"])
    def handle_write(task):
        return "text"

    tags = registry.get_tags()
    assert "#SKILL_CODE" in tags
    assert "#SKILL_WRITE" in tags


def test_can_handle():
    """Test checking if registry can handle tasks."""
    registry = SkillRegistry()

    @registry.register("code", tags=["#SKILL_CODE", "#SKILL_PYTHON"])
    def handle_code(task):
        return "code"

    assert registry.can_handle(["#SKILL_CODE"]) is True
    assert registry.can_handle(["#SKILL_WRITE"]) is False


def test_find_handler():
    """Test finding a handler for task skills."""
    registry = SkillRegistry()

    @registry.register("code", tags=["#SKILL_CODE"])
    def handle_code(task):
        return "code"

    handler = registry.find_handler(["#SKILL_CODE"])
    assert handler is not None
    assert handler(None) == "code"

    handler = registry.find_handler(["#SKILL_WRITE"])
    assert handler is None
