#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moltswarm.client import MoltbookClient
from moltswarm.protocols import Task
from moltswarm.executors import RuleBasedExecutor
from datetime import datetime, timedelta

API_KEY = os.getenv("MOLTBOOK_API_KEY")
if not API_KEY:
    print("Error: MOLTBOOK_API_KEY not set")
    sys.exit(1)

def main():
    print("=" * 60)
    print("🐝 MoltSwarm Live Test")
    print("=" * 60)
    print()

    client = MoltbookClient(api_key=API_KEY)
    executor = RuleBasedExecutor()

    # Step 1: Create a test task
    print("Step 1: Creating test task...")
    task = Task(
        version="1.0",
        job_id=f"live_test_{int(datetime.now().timestamp())}",
        type="write",
        skills=["#SKILL_WRITE"],
        reward_karma=True,
        claim_timeout=3600,
        deadline=(datetime.now() + timedelta(hours=24)).isoformat(),
        title="Hello from MoltSwarm",
        description="This is a test to see if our node works",
        requirements=["Say hello back"],
        output_format="text",
        validation="",
        post_id="",
        post_url="",
        author="",
    )

    result = client.create_post(
        submolt="general",
        title=f"[SWARM_JOB] {task.title}",
        content=task.to_markdown(),
    )

    post_id = result['post']['id']
    print(f"✅ Task created!")
    print(f"   Post ID: {post_id}")
    print(f"   URL: https://www.moltbook.com/posts/{post_id}")
    print()

    # Step 2: Discover the task
    print("Step 2: Discovering tasks from feed...")
    feed = client.get_feed(sort="new", limit=50)

    found_tasks = []
    for post in feed:
        parsed = Task.from_post(post)
        if parsed:
            found_tasks.append(parsed)

    print(f"Found {len(found_tasks)} swarm jobs")

    # Find our specific task
    our_task = None
    for t in found_tasks:
        if t.job_id == task.job_id:
            our_task = t
            break

    if our_task:
        print(f"✅ Found our task: {our_task.title}")
    else:
        print("⚠️  Task not in feed yet (might take a moment)")
        # Try to get it directly
        try:
            post = client.get_post(post_id)
            our_task = Task.from_post(post)
            if our_task:
                print(f"✅ Found task via direct lookup")
        except:
            pass
    print()

    # Step 3: Claim the task
    if our_task:
        print("Step 3: Claiming task...")
        from moltswarm.protocols import TaskDelivery

        claim = TaskDelivery(
            job_id=our_task.job_id,
            status="CLAIMING"
        )

        client.add_comment(our_task.post_id, claim.to_comment())
        print(f"✅ Task claimed!")
        print()

        # Step 4: Execute the task
        print("Step 4: Executing task...")
        result = executor.execute(our_task)
        print("Generated result:")
        print("-" * 40)
        print(result[:200])
        print("-" * 40)
        print()

        # Step 5: Deliver result
        print("Step 5: Delivering result...")
        delivery = TaskDelivery(
            job_id=our_task.job_id,
            status="DELIVERED",
            result=result
        )

        client.add_comment(our_task.post_id, delivery.to_comment())
        print("✅ Result delivered!")
        print()

        # Step 6: Upvote
        print("Step 6: Upvoting post...")
        client.upvote_post(our_task.post_id)
        print("✅ Upvoted!")
        print()

    print("=" * 60)
    print("✅ Live test complete!")
    print("=" * 60)
    print()
    print(f"🔗 View the task:")
    print(f"   https://www.moltbook.com/posts/{post_id}")
    print()

if __name__ == "__main__":
    main()
