#!/usr/bin/env python3
"""
Test Moltbook API calls with real API key.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moltswarm.client import MoltbookClient

# Get API key from environment
API_KEY = os.getenv("MOLTBOOK_API_KEY")
if not API_KEY:
    print("❌ Error: MOLTBOOK_API_KEY environment variable not set")
    print()
    print("Usage:")
    print("  MOLTBOOK_API_KEY=your_key python scripts/test_api.py")
    print()
    print("Or set it first:")
    print("  export MOLTBOOK_API_KEY=your_key")
    sys.exit(1)

def test_api():
    """Test various Moltbook API endpoints."""
    print("=" * 60)
    print("Testing Moltbook API")
    print("=" * 60)
    print()

    client = MoltbookClient(api_key=API_KEY)

    # Test 1: Get profile
    print("1️⃣ Testing: Get Profile")
    print("-" * 40)
    try:
        profile = client.get_profile()
        print(f"✅ Success!")
        print(f"   Name: {profile.get('agent', {}).get('name')}")
        print(f"   Description: {profile.get('agent', {}).get('description')}")
        print(f"   Karma: {profile.get('agent', {}).get('karma')}")
        print(f"   Status: {profile.get('agent', {}).get('status')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()

    # Test 2: Get feed
    print("2️⃣ Testing: Get Feed")
    print("-" * 40)
    try:
        feed = client.get_feed(sort="new", limit=5)
        print(f"✅ Success! Retrieved {len(feed)} posts")
        if feed:
            print(f"   Latest post: {feed[0].get('title', 'No title')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()

    # Test 3: Search posts
    print("3️⃣ Testing: Search Posts")
    print("-" * 40)
    try:
        results = client.search_posts("python", limit=5)
        print(f"✅ Success! Found {len(results)} results")
        if results:
            print(f"   Top result: {results[0].get('title', 'No title')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()

    # Test 4: Get comments (using a post ID if available)
    print("4️⃣ Testing: Get Comments")
    print("-" * 40)
    try:
        feed = client.get_feed(sort="new", limit=1)
        if feed:
            post_id = feed[0].get('id')
            comments = client.get_comments(post_id)
            print(f"✅ Success! Post '{feed[0].get('title')}' has {len(comments)} comments")
        else:
            print("⚠️  No posts available to test comments")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()

    # Test 5: Check agent status
    print("5️⃣ Testing: Agent Status")
    print("-" * 40)
    try:
        status = client._request("GET", "agents/status")
        print(f"✅ Success!")
        print(f"   Status: {status.get('status')}")
        if status.get('status') == 'pending_claim':
            print("   ℹ️  Agent needs to be claimed via Twitter")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()

    print("=" * 60)
    print("API Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_api()
