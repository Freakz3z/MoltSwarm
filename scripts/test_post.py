#!/usr/bin/env python3
"""
Test creating a swarm job post on Moltbook.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moltswarm.client import MoltbookClient
from moltswarm.protocols import Task
from datetime import datetime, timedelta

API_KEY = os.getenv("MOLTBOOK_API_KEY")
if not API_KEY:
    print("Error: MOLTBOOK_API_KEY not set")
    sys.exit(1)

def test_create_swarm_job():
    """Test creating a swarm job post."""
    print("=" * 60)
    print("Testing: Create Swarm Job Post")
    print("=" * 60)
    print()

    client = MoltbookClient(api_key=API_KEY)

    # Create a test task
    task = Task(
        version="1.0",
        job_id=f"test_job_{int(datetime.now().timestamp())}",
        type="code",
        skills=["#SKILL_CODE", "#SKILL_PYTHON"],
        reward_karma=True,
        claim_timeout=3600,
        deadline=(datetime.now() + timedelta(hours=24)).isoformat(),
        title="Hello World Function",
        description="Write a Python function that prints 'Hello, World!'",
        requirements=["Python 3.8+", "Simple function"],
        output_format="code_block",
        validation="Function should print 'Hello, World!'",
        post_id="",  # Will be set after posting
        post_url="",
        author="",
    )

    content = task.to_markdown()

    print("📝 Creating swarm job post...")
    print(f"   Title: {task.title}")
    print(f"   Job ID: {task.job_id}")
    print()

    try:
        result = client.create_post(
            submolt="general",
            title=f"[SWARM_JOB] {task.title}",
            content=content,
        )

        print("✅ Post created successfully!")
        print()
        print("📋 Post Details:")
        print(f"   Post ID: {result['post']['id']}")
        print(f"   URL: https://www.moltbook.com/posts/{result['post']['id']}")
        print()
        print("🔗 View your post at:")
        print(f"   https://www.moltbook.com/posts/{result['post']['id']}")
        print()

        return result

    except Exception as e:
        print(f"❌ Error creating post: {e}")
        print()
        print("ℹ️  This is expected if the agent is not yet claimed.")
        print("   Claim your agent at the URL provided during registration.")
        return None

    print("=" * 60)

if __name__ == "__main__":
    test_create_swarm_job()
