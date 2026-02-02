"""
Run a live test of the MoltSwarm node.

This will:
1. Start the node
2. Discover tasks on Moltbook
3. Process matching tasks
4. Deliver results

Press Ctrl+C to stop.
"""

import os
from moltswarm import SwarmNode
from moltswarm.protocols import Task
from moltswarm.executors import RuleBasedExecutor

# API key
API_KEY = os.getenv("MOLTBOOK_API_KEY")
if not API_KEY:
    print("Error: MOLTBOOK_API_KEY not set")
    sys.exit(1)

def main():
    print("=" * 60)
    print("🐝 MoltSwarm Live Test")
    print("=" * 60)
    print()

    # Create node
    node = SwarmNode(
        name="MoltSwarmTest",
        skills=["write", "summarize", "code"],
        api_key=API_KEY,
        description="Testing MoltSwarm with real tasks",
        auto_claim=True,
    )

    # Use rule-based executor
    executor = RuleBasedExecutor()

    @node.skill("write", tags=["#SKILL_WRITE"])
    def handle_write(task: Task):
        print(f"  📝 Writing task: {task.title}")
        result = executor.execute(task)
        print(f"  ✅ Generated response")
        return result

    @node.skill("summarize", tags=["#SKILL_SUMMARIZE"])
    def handle_summarize(task: Task):
        print(f"  📊 Summarizing task: {task.title}")
        result = executor.execute(task)
        print(f"  ✅ Generated summary")
        return result

    @node.skill("code", tags=["#SKILL_CODE"])
    def handle_code(task: Task):
        print(f"  💻 Coding task: {task.title}")
        result = executor.execute(task)
        print(f"  ✅ Generated code")
        return result

    print("🚀 Starting node...")
    print(f"   Name: {node.name}")
    print(f"   Skills: {', '.join(node.skills)}")
    print(f"   Check interval: 60 seconds")
    print()
    print("📡 Listening for tasks...")
    print("   (This will check Moltbook for matching tasks every minute)")
    print()
    print("💡 Tip: Press Ctrl+C to stop")
    print()
    print("=" * 60)
    print()

    try:
        # Start with shorter interval for testing (60 seconds)
        node.start(check_interval=60)
    except KeyboardInterrupt:
        print()
        print("=" * 60)
        print("🛑 Node stopped by user")
        print("=" * 60)

if __name__ == "__main__":
    main()
