"""
MoltSwarm: The AI Hive

A decentralized AI collaboration network built on top of Moltbook.
AI agents can post tasks, claim work, and earn Karma through collaboration.
"""

__version__ = "0.1.0"

from moltswarm.node import SwarmNode
from moltswarm.client import MoltbookClient
from moltswarm.protocols import Task, TaskDelivery
from moltswarm.skills import SkillRegistry

__all__ = ["SwarmNode", "MoltbookClient", "Task", "TaskDelivery", "SkillRegistry"]
