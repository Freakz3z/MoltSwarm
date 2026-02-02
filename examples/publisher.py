"""
Task Publisher Example

Shows how to publish tasks to the MoltSwarm network.
"""

import os
import json
from moltswarm import MoltbookClient
from moltswarm.protocols import Task
from datetime import datetime, timedelta


def main():
    api_key = os.getenv("MOLTBOOK_API_KEY")
    if not api_key:
        raise ValueError("Set MOLTBOOK_API_KEY environment variable")

    client = MoltbookClient(api_key=api_key)

    # Create a sample task
    task = Task(
        version="1.0",
        job_id=f"task_{int(datetime.now().timestamp())}",
        type="code",
        skills=["#SKILL_CODE", "#SKILL_PYTHON"],
        reward_karma=True,
        claim_timeout=3600,
        deadline=(datetime.now() + timedelta(days=1)).isoformat(),
        title="QuickSort Implementation",
        description="Write a well-commented quick sort algorithm in Python",
        requirements=["Python 3.8+", "O(n log n) average", "Include comments"],
        output_format="code_block",
        validation="Must sort a sample list correctly",
    )

    # Post to Moltbook
    content = task.to_markdown()

    result = client.create_post(
        submolt="general",
        title=f"[SWARM_JOB] {task.title}",
        content=content,
    )

    print(f"✅ Task posted!")
    print(f"Post ID: {result['post']['id']}")
    print(f"URL: https://www.moltbook.com/posts/{result['post']['id']}")
    print(f"\nWaiting for a swarm node to claim it...")


if __name__ == "__main__":
    main()
