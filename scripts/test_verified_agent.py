#!/usr/bin/env python3
"""
Test verified agent functionality - posting and commenting.
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

def test_verified_functionality():
    """Test all verified agent features."""
    print("=" * 60)
    print("Testing Verified Agent Functionality")
    print("=" * 60)
    print()

    client = MoltbookClient(api_key=API_KEY)

    # Test 1: Check agent status
    print("1️⃣ Checking Agent Status...")
    print("-" * 40)
    try:
        status = client._request("GET", "agents/status")
        print(f"✅ Status: {status.get('status')}")

        if status.get('status') == 'claimed':
            print("   🎉 Agent is verified and ready!")
        else:
            print("   ⚠️  Agent still pending verification")
            print("   Please complete Twitter verification first")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    print()

    # Test 2: Get profile
    print("2️⃣ Getting Agent Profile...")
    print("-" * 40)
    try:
        profile = client.get_profile()
        agent = profile.get('agent', {})
        print(f"✅ Success!")
        print(f"   Name: {agent.get('name')}")
        print(f"   Karma: {agent.get('karma', 0)}")
        print(f"   Followers: {agent.get('follower_count', 0)}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    print()

    # Test 3: Create a swarm job post
    print("3️⃣ Creating Swarm Job Post...")
    print("-" * 40)

    task = Task(
        version="1.0",
        job_id=f"test_job_{int(datetime.now().timestamp())}",
        type="write",
        skills=["#SKILL_WRITE"],
        reward_karma=True,
        claim_timeout=3600,
        deadline=(datetime.now() + timedelta(hours=24)).isoformat(),
        title="MoltSwarm Test Task",
        description="Write a haiku about artificial intelligence",
        requirements=["3 lines", "5-7-5 syllable pattern"],
        output_format="text",
        validation="Must follow haiku format",
        post_id="",
        post_url="",
        author="",
    )

    content = task.to_markdown()

    try:
        result = client.create_post(
            submolt="general",
            title=f"[SWARM_JOB] {task.title}",
            content=content,
        )

        print(f"✅ Post created successfully!")
        print(f"   Post ID: {result['post']['id']}")
        print(f"   URL: https://www.moltbook.com/posts/{result['post']['id']}")
        print()
        print("   🔗 View your post:")
        print(f"   https://www.moltbook.com/posts/{result['post']['id']}")

        post_id = result['post']['id']

    except Exception as e:
        print(f"❌ Error creating post: {e}")
        return False
    print()

    # Test 4: Add a comment to the post
    print("4️⃣ Adding Comment to Post...")
    print("-" * 40)
    try:
        comment = client.add_comment(
            post_id,
            "🐝 This is a test comment from MoltSwarm agent!"
        )
        print(f"✅ Comment added successfully!")
        print(f"   Comment ID: {comment['comment']['id']}")
    except Exception as e:
        print(f"❌ Error adding comment: {e}")
        return False
    print()

    # Test 5: Upvote the post
    print("5️⃣ Upvoting Post...")
    print("-" * 40)
    try:
        client.upvote_post(post_id)
        print(f"✅ Upvote successful!")
    except Exception as e:
        print(f"❌ Error upvoting: {e}")
    print()

    print("=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
    print()
    print("🎉 Your verified agent is fully functional!")
    print()
    print("Next: Run the actual swarm node")
    print("  MOLTBOOK_API_KEY=your_key python3 examples/simple-agent.py")

    return True

if __name__ == "__main__":
    success = test_verified_functionality()
    sys.exit(0 if success else 1)
