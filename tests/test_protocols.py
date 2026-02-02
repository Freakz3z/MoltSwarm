"""Tests for MoltSwarm protocols."""

import pytest
import json
from moltswarm.protocols import Task, TaskDelivery, find_existing_claim, is_claim_expired


def test_task_from_post():
    """Test parsing a task from a post."""
    post_data = {
        "id": "post_123",
        "author": {"name": "TestUser"},
        "content": """
# [SWARM_JOB] Test Task

This is a test task.

```json
{
  "swarm": {
    "version": "1.0",
    "job_id": "job_abc123",
    "type": "code",
    "skills": ["#SKILL_CODE", "#SKILL_PYTHON"],
    "reward_karma": true,
    "claim_timeout": 3600
  },
  "task": {
    "title": "Test Task",
    "description": "This is a test task",
    "requirements": ["req1", "req2"],
    "output_format": "code_block",
    "validation": "must pass tests"
  }
}
```
"""
    }

    task = Task.from_post(post_data)

    assert task is not None
    assert task.job_id == "job_abc123"
    assert task.type == "code"
    assert "#SKILL_CODE" in task.skills
    assert task.reward_karma is True
    assert task.post_id == "post_123"


def test_task_from_post_without_swarm():
    """Test that non-swarm posts return None."""
    post_data = {
        "id": "post_123",
        "content": "Just a regular post"
    }

    task = Task.from_post(post_data)
    assert task is None


def test_task_matches_skills():
    """Test skill matching."""
    task = Task(
        version="1.0",
        job_id="test",
        type="code",
        skills=["#SKILL_CODE", "#SKILL_PYTHON"],
        reward_karma=True,
        claim_timeout=3600,
        title="Test"
    )

    assert task.matches_skills(["code", "python"]) is True
    assert task.matches_skills(["write"]) is False
    assert task.matches_skills(["#SKILL_CODE"]) is True


def test_task_delivery_claiming():
    """Test claim delivery format."""
    delivery = TaskDelivery(
        job_id="job_123",
        status="CLAIMING",
        result=""
    )

    comment = delivery.to_comment()

    assert "CLAIMING" in comment
    assert "job_id=job_123" in comment


def test_task_delivery_delivered():
    """Test delivered delivery format."""
    delivery = TaskDelivery(
        job_id="job_123",
        status="DELIVERED",
        result="Here is the result",
        delivered_at="2025-02-03T12:00:00Z"
    )

    comment = delivery.to_comment()

    assert "DELIVERED" in comment
    assert "job_id=job_123" in comment
    assert "Here is the result" in comment


def test_find_existing_claim():
    """Test finding existing claims."""
    comments = [
        {"content": "Great post!", "created_at": "2025-02-03T10:00:00Z"},
        {"content": "🐝 **CLAIMING**: `job_id=job_123`", "created_at": "2025-02-03T11:00:00Z"},
        {"content": "Another comment", "created_at": "2025-02-03T12:00:00Z"},
    ]

    claim = find_existing_claim(comments, "job_123")

    assert claim is not None
    assert "CLAIMING" in claim["content"]


def test_find_existing_claim_not_found():
    """Test when no claim exists."""
    comments = [
        {"content": "Great post!", "created_at": "2025-02-03T10:00:00Z"},
    ]

    claim = find_existing_claim(comments, "job_123")

    assert claim is None


def test_task_to_markdown():
    """Test converting task to markdown."""
    task = Task(
        version="1.0",
        job_id="job_123",
        type="code",
        skills=["#SKILL_CODE"],
        reward_karma=True,
        claim_timeout=3600,
        title="Test Task",
        description="Test description"
    )

    markdown = task.to_markdown()

    assert "# [SWARM_JOB] Test Task" in markdown
    assert "job_123" in markdown
    assert "#SKILL_CODE" in markdown
