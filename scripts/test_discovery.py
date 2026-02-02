#!/usr/bin/env python3
"""
Test task discovery from Moltbook feed.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moltswarm.client import MoltbookClient
from moltswarm.protocols import Task

API_KEY = os.getenv("MOLTBOOK_API_KEY")
if not API_KEY:
    print("Error: MOLTBOOK_API_KEY not set")
    sys.exit(1)

def test_task_discovery():
    """Test discovering tasks from feed."""
    print("=" * 60)
    print("Testing Task Discovery")
    print("=" * 60)
    print()

    client = MoltbookClient(api_key=API_KEY)

    # Get feed
    print("📡 Fetching feed...")
    feed = client.get_feed(sort="new", limit=25)
    print(f"✅ Got {len(feed)} posts")
    print()

    # Look for swarm jobs
    print("🔍 Looking for #SWARM_JOB posts...")
    swarm_jobs = []

    for post in feed:
        task = Task.from_post(post)
        if task:
            swarm_jobs.append(task)
            print(f"   Found: {task.title} (job_id: {task.job_id})")

    print()
    print(f"📊 Results:")
    print(f"   Total posts: {len(feed)}")
    print(f"   Swarm jobs: {len(swarm_jobs)}")

    if swarm_jobs:
        print()
        print("🐝 Swarm Job Details:")
        for i, task in enumerate(swarm_jobs[:3], 1):
            print(f"   {i}. {task.title}")
            print(f"      Type: {task.type}")
            print(f"      Skills: {task.skills}")
            print(f"      Reward: {task.reward_karma}")
            print()

    # Test parsing a mock swarm job
    print("🧪 Testing mock swarm job parsing...")
    mock_post = {
        "id": "test_123",
        "author": {"name": "TestUser"},
        "content": """
# [SWARM_JOB] Write a Python function

I need a function that sorts a list.

```json
{
  "swarm": {
    "version": "1.0",
    "job_id": "test_job_xyz",
    "type": "code",
    "skills": ["#SKILL_CODE", "#SKILL_PYTHON"],
    "reward_karma": true,
    "claim_timeout": 3600
  },
  "task": {
    "title": "Sort Function",
    "description": "Write a function to sort a list",
    "requirements": ["Python 3.8+"],
    "output_format": "code_block",
    "validation": "Must work with integers"
  }
}
```
"""
    }

    task = Task.from_post(mock_post)
    if task:
        print("✅ Mock job parsed successfully!")
        print(f"   Job ID: {task.job_id}")
        print(f"   Skills: {task.skills}")
        print(f"   Matches ['code', 'python']: {task.matches_skills(['code', 'python'])}")
    else:
        print("❌ Failed to parse mock job")

    print()
    print("=" * 60)

if __name__ == "__main__":
    test_task_discovery()
