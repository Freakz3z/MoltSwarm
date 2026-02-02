"""Configuration management for MoltSwarm."""

import os
import yaml
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class MoltbookConfig:
    """Moltbook API configuration."""
    api_key: str
    base_url: str = "https://www.moltbook.com/api/v1"


@dataclass
class NodeConfig:
    """Swarm node configuration."""
    name: str
    description: str = ""
    skills: list = field(default_factory=list)
    heartbeat_interval: int = 14400  # 4 hours
    auto_claim: bool = True


@dataclass
class SwarmConfig:
    """Main MoltSwarm configuration."""
    moltbook: MoltbookConfig
    node: NodeConfig

    @classmethod
    def from_file(cls, path: str) -> "SwarmConfig":
        """Load config from YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f)

        return cls(
            moltbook=MoltbookConfig(**data["moltbook"]),
            node=NodeConfig(**data["swarm_node"]),
        )

    @classmethod
    def from_env(cls) -> "SwarmConfig":
        """Load config from environment variables."""
        api_key = os.getenv("MOLTBOOK_API_KEY")
        if not api_key:
            raise ValueError("MOLTBOOK_API_KEY environment variable not set")

        return cls(
            moltbook=MoltbookConfig(api_key=api_key),
            node=NodeConfig(
                name=os.getenv("SWARM_NODE_NAME", "AIWorker"),
                description=os.getenv("SWARM_NODE_DESC", ""),
                skills=os.getenv("SWARM_NODE_SKILLS", "").split(","),
            ),
        )

    @classmethod
    def auto_load(cls) -> "SwarmConfig":
        """Auto-detect and load config from file or env."""
        # Try config file first
        config_paths = [
            "config.yaml",
            "config.yml",
            os.path.expanduser("~/.config/moltswarm/config.yaml"),
        ]

        for path in config_paths:
            if Path(path).exists():
                return cls.from_file(path)

        # Fall back to environment
        return cls.from_env()
