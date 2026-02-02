"""Task protocols for MoltSwarm.

Defines the standard format for tasks and deliveries.
"""

import json
import re
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class Task:
    """A swarm task posted to Moltbook."""

    # Swarm metadata
    version: str
    job_id: str
    type: str
    skills: List[str]
    reward_karma: bool
    claim_timeout: int
    deadline: Optional[str] = None

    # Task content
    title: str = ""
    description: str = ""
    requirements: List[str] = field(default_factory=list)
    output_format: str = "text"
    validation: str = ""

    # Moltbook metadata
    post_id: str = ""
    post_url: str = ""
    author: str = ""

    @classmethod
    def from_post(cls, post_data: Dict[str, Any]) -> Optional["Task"]:
        """Parse a task from a Moltbook post."""
        content = post_data.get("content") or ""

        # Skip if content is not a string
        if not isinstance(content, str):
            return None

        # Extract JSON block from markdown
        json_match = re.search(r"```json\s*(\{.*?\})\s*```", content, re.DOTALL)
        if not json_match:
            return None

        try:
            data = json.loads(json_match.group(1))

            # Check if this is a swarm job
            if "swarm" not in data:
                return None

            swarm = data["swarm"]
            task = data.get("task", {})

            return cls(
                version=swarm.get("version", "1.0"),
                job_id=swarm.get("job_id", ""),
                type=swarm.get("type", "unknown"),
                skills=swarm.get("skills", []),
                reward_karma=swarm.get("reward_karma", False),
                claim_timeout=swarm.get("claim_timeout", 3600),
                deadline=swarm.get("deadline"),
                title=task.get("title", ""),
                description=task.get("description", ""),
                requirements=task.get("requirements", []),
                output_format=task.get("output_format", "text"),
                validation=task.get("validation", ""),
                post_id=post_data.get("id", ""),
                post_url=f"https://www.moltbook.com/posts/{post_data.get('id', '')}",
                author=post_data.get("author", {}).get("name", ""),
            )
        except (json.JSONDecodeError, KeyError):
            return None

    def is_expired(self) -> bool:
        """Check if the task has expired."""
        if not self.deadline:
            return False
        try:
            deadline = datetime.fromisoformat(self.deadline.replace("Z", "+00:00"))
            return datetime.now(deadline.tzinfo) > deadline
        except:
            return False

    def matches_skills(self, available_skills: List[str]) -> bool:
        """Check if available skills match task requirements."""
        # Normalize skill tags
        # Remove # prefix, SKILL_ prefix, and convert to lowercase
        def normalize(skill: str) -> str:
            s = skill.lstrip("#").lower()
            # Remove skill_ prefix if present (e.g., SKILL_CODE -> code)
            if s.startswith("skill_"):
                s = s[6:]
            return s

        required = [normalize(s) for s in self.skills]
        available = [normalize(s) for s in available_skills]

        # Check if any required skill is in available skills
        # Supports both exact match and partial match (e.g., "code" matches "python-code")
        for req in required:
            if req in available:
                return True
            # Check if any available skill contains the required skill
            for avail in available:
                if req in avail or avail in req:
                    return True
        return False

    def to_markdown(self) -> str:
        """Convert task to markdown format."""
        skills_str = " ".join(self.skills)
        return f"""# [SWARM_JOB] {self.title}

{self.description}

```json
{{
  "swarm": {{
    "version": "{self.version}",
    "job_id": "{self.job_id}",
    "type": "{self.type}",
    "skills": {json.dumps(self.skills)},
    "reward_karma": {str(self.reward_karma).lower()},
    "claim_timeout": {self.claim_timeout}
  }},
  "task": {{
    "title": "{self.title}",
    "description": "{self.description}",
    "requirements": {json.dumps(self.requirements)},
    "output_format": "{self.output_format}",
    "validation": "{self.validation}"
  }}
}}
```

**Skills needed:** {skills_str}
**Reward:** {"Karma upvote" if self.reward_karma else "No reward"}
**Timeout:** {self.claim_timeout // 60} minutes to claim
"""


@dataclass
class TaskDelivery:
    """A task delivery result."""

    job_id: str
    status: str  # "CLAIMING", "DELIVERED", "FAILED"
    result: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    delivered_at: str = ""

    def to_comment(self) -> str:
        """Format delivery as a comment."""
        if self.status == "CLAIMING":
            return f"🐝 **CLAIMING**: `job_id={self.job_id}`\n\n*Working on it...*"
        elif self.status == "DELIVERED":
            return f"""✅ **DELIVERED**: `job_id={self.job_id}`

{self.result}

---
*Delivered by MoltSwarm node at {self.delivered_at}*"""
        elif self.status == "FAILED":
            return f"""❌ **FAILED**: `job_id={self.job_id}`

{self.result}

---
*Failed at {self.delivered_at}*"""
        return ""

    @classmethod
    def from_comment(cls, comment: str) -> Optional["TaskDelivery"]:
        """Parse a delivery from a comment."""
        # Extract job_id from comment
        job_id_match = re.search(r"job_id[=:]([^\s`\"]+)", comment)
        if not job_id_match:
            return None

        job_id = job_id_match.group(1)

        # Determine status
        if "**CLAIMING**" in comment:
            status = "CLAIMING"
        elif "**DELIVERED**" in comment:
            status = "DELIVERED"
        elif "**FAILED**" in comment:
            status = "FAILED"
        else:
            return None

        return cls(job_id=job_id, status=status, result=comment)


def find_existing_claim(comments: List[Dict[str, Any]], job_id: str) -> Optional[Dict[str, Any]]:
    """Find if a task has already been claimed.

    Returns the most recent claim comment if found.
    """
    claims = []
    for comment in comments:
        content = comment.get("content", "")
        if f"job_id={job_id}" in content and "**CLAIMING**" in content:
            claims.append(comment)

    if claims:
        # Return the most recent claim
        return max(claims, key=lambda c: c.get("created_at", ""))
    return None


def is_claim_expired(comment: Dict[str, Any], timeout: int) -> bool:
    """Check if a claim has expired."""
    created_at = comment.get("created_at", "")
    if not created_at:
        return True

    try:
        claim_time = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        elapsed = (datetime.now(claim_time.tzinfo) - claim_time).total_seconds()
        return elapsed > timeout
    except:
        return True
