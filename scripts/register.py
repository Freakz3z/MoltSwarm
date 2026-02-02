#!/usr/bin/env python3
"""
Register a new agent on Moltbook and get API key.

Usage:
    python3 scripts/register.py "YourAgentName" "Description of what your agent does"
"""

import sys
import requests
import json


def register_agent(name: str, description: str):
    """Register a new agent on Moltbook."""
    url = "https://www.moltbook.com/api/v1/agents/register"

    payload = {
        "name": name,
        "description": description
    }

    print(f"🦞 Registering agent '{name}' on Moltbook...")
    print(f"   Description: {description}")
    print()

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()

        data = response.json()

        if "agent" in data:
            agent = data["agent"]

            print("✅ Registration successful!")
            print()
            print("=" * 60)
            print("📋 SAVE THIS INFORMATION:")
            print("=" * 60)
            print()
            print(f"Agent Name: {name}")
            print(f"API Key:    {agent['api_key']}")
            print(f"Claim URL:  {agent['claim_url']}")
            print(f"Verify Code: {agent.get('verification_code', 'N/A')}")
            print()
            print("=" * 60)
            print()
            print("🔔 Next Steps:")
            print("1. Save your API key immediately!")
            print("2. Visit the claim URL to verify with X (Twitter)")
            print("3. Create a config.yaml file with your API key:")
            print()
            print("   moltbook:")
            print(f"     api_key: \"{agent['api_key']}\"")
            print()
            print("4. Or set environment variable:")
            print()
            print(f"   export MOLTBOOK_API_KEY=\"{agent['api_key']}\"")
            print()

            return agent

        else:
            print("❌ Unexpected response format")
            print(json.dumps(data, indent=2))
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Registration failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Status: {e.response.status_code}")
            try:
                print(f"   Error: {e.response.json()}")
            except:
                print(f"   Body: {e.response.text[:200]}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/register.py <AgentName> [Description]")
        print()
        print("Example:")
        print("  python3 scripts/register.py MyAgent \"AI coding assistant\"")
        sys.exit(1)

    name = sys.argv[1]
    description = sys.argv[2] if len(sys.argv) > 2 else f"AI agent named {name}"

    register_agent(name, description)
