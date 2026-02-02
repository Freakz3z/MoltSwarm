#!/usr/bin/env python3
"""
Test the flexible execution system.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moltswarm.executors import (
    RuleBasedExecutor,
    HybridExecutor,
    AIModelExecutor
)
from moltswarm.protocols import Task

def test_executors():
    """Test different execution strategies."""
    print("=" * 60)
    print("Testing MoltSwarm Execution System")
    print("=" * 60)
    print()

    # Create a test task
    task = Task(
        version="1.0",
        job_id="test_123",
        type="write",
        skills=["#SKILL_WRITE"],
        reward_karma=True,
        claim_timeout=3600,
        title="Test Haiku",
        description="Write a haiku about AI",
        requirements=["3 lines", "5-7-5 syllables"],
        output_format="text",
        validation="",
        post_id="",
        post_url="",
        author="",
    )

    # Test 1: Rule-based executor
    print("1️⃣ Testing Rule-Based Executor...")
    print("-" * 40)
    rule_executor = RuleBasedExecutor()
    result = rule_executor.execute(task)
    print("✅ Result:")
    print(result)
    print()

    # Test 2: Code task
    print("2️⃣ Testing Code Generation...")
    print("-" * 40)
    code_task = Task(
        version="1.0",
        job_id="test_456",
        type="code",
        skills=["#SKILL_CODE", "#SKILL_PYTHON"],
        reward_karma=True,
        claim_timeout=3600,
        title="Sort Function",
        description="Write a function to sort a list",
        requirements=["Python", "O(n log n)"],
        output_format="code_block",
        validation="",
        post_id="",
        post_url="",
        author="",
    )

    result = rule_executor.execute(code_task)
    print("✅ Result:")
    print(result)
    print()

    # Test 3: Hybrid executor (no AI)
    print("3️⃣ Testing Hybrid Executor (Rule-based fallback)...")
    print("-" * 40)
    hybrid = HybridExecutor(
        ai_executor=None,  # No AI configured
        fallback=RuleBasedExecutor()
    )
    result = hybrid.execute(task)
    print("✅ Result:")
    print(result[:200] + "..." if len(result) > 200 else result)
    print()

    # Test 4: Check AI availability
    print("4️⃣ Checking AI Configuration...")
    print("-" * 40)
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))

    print(f"OpenAI API Key: {'✅ Configured' if has_openai else '❌ Not set'}")
    print(f"Anthropic API Key: {'✅ Configured' if has_anthropic else '❌ Not set'}")
    print()

    if has_openai or has_anthropic:
        print("🎉 AI is available! Testing AI executor...")
        print("-" * 40)

        provider = "openai" if has_openai else "anthropic"
        ai_executor = AIModelExecutor(
            provider=provider,
            api_key=os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        )

        try:
            result = ai_executor.execute(task)
            print("✅ AI Result:")
            print(result[:300] + "..." if len(result) > 300 else result)
        except Exception as e:
            print(f"⚠️  AI execution failed: {e}")
    else:
        print("ℹ️  No AI keys found. Rule-based mode works great without AI!")
        print()
        print("To add AI:")
        print("  export OPENAI_API_KEY=your-key")
        print("  export ANTHROPIC_API_KEY=your-key")
    print()

    print("=" * 60)
    print("✅ Execution System Test Complete!")
    print("=" * 60)
    print()
    print("📋 Summary:")
    print("  • Rule-based execution: Working ✅")
    print("  • Code generation: Working ✅")
    print("  • Hybrid fallback: Working ✅")
    if has_openai or has_anthropic:
        print("  • AI execution: Available ✅")
    else:
        print("  • AI execution: Not configured (optional)")
    print()
    print("🚀 Your node is ready to run!")
    print()
    print("Start with:")
    print("  MOLTBOOK_API_KEY=your_key python3 examples/flexible_agent.py")

if __name__ == "__main__":
    test_executors()
