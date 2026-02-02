"""Moltbook API client for MoltSwarm."""

import time
import requests
from typing import Optional, Dict, Any, List


class MoltbookClient:
    """Client for interacting with Moltbook API."""

    def __init__(self, api_key: str, base_url: str = "https://www.moltbook.com/api/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an API request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.request(method, url, **kwargs)

        if response.status_code == 429:
            # Rate limited
            data = response.json()
            retry_after = data.get("retry_after_seconds", 60)
            print(f"Rate limited. Waiting {retry_after}s...")
            time.sleep(retry_after)
            return self._request(method, endpoint, **kwargs)

        response.raise_for_status()
        return response.json()

    # Agent methods

    def get_profile(self) -> Dict[str, Any]:
        """Get your agent profile."""
        return self._request("GET", "agents/me")

    def update_profile(self, description: Optional[str] = None) -> Dict[str, Any]:
        """Update your profile description."""
        data = {}
        if description:
            data["description"] = description
        return self._request("PATCH", "agents/me", json=data)

    # Post methods

    def create_post(
        self,
        submolt: str,
        title: str,
        content: str,
        url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new post."""
        data = {"submolt": submolt, "title": title, "content": content}
        if url:
            data["url"] = url
        return self._request("POST", "posts", json=data)

    def get_post(self, post_id: str) -> Dict[str, Any]:
        """Get a single post."""
        return self._request("GET", f"posts/{post_id}")

    def get_feed(
        self,
        sort: str = "new",
        limit: int = 25,
        submolt: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get feed of posts."""
        params = {"sort": sort, "limit": limit}
        if submolt:
            params["submolt"] = submolt

        result = self._request("GET", "posts", params=params)
        return result.get("posts", [])

    def get_personalized_feed(self, sort: str = "new", limit: int = 25) -> List[Dict[str, Any]]:
        """Get your personalized feed."""
        result = self._request("GET", "feed", params={"sort": sort, "limit": limit})
        return result.get("posts", [])

    def search_posts(
        self,
        query: str,
        post_type: str = "posts",
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Semantic search for posts."""
        result = self._request(
            "GET",
            "search",
            params={"q": query, "type": post_type, "limit": limit}
        )
        return result.get("results", [])

    # Comment methods

    def add_comment(
        self,
        post_id: str,
        content: str,
        parent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add a comment to a post."""
        data = {"content": content}
        if parent_id:
            data["parent_id"] = parent_id
        return self._request("POST", f"posts/{post_id}/comments", json=data)

    def get_comments(self, post_id: str, sort: str = "new") -> List[Dict[str, Any]]:
        """Get comments on a post."""
        result = self._request("GET", f"posts/{post_id}/comments", params={"sort": sort})
        return result.get("comments", [])

    # Voting methods

    def upvote_post(self, post_id: str) -> Dict[str, Any]:
        """Upvote a post."""
        return self._request("POST", f"posts/{post_id}/upvote")

    def upvote_comment(self, comment_id: str) -> Dict[str, Any]:
        """Upvote a comment."""
        return self._request("POST", f"comments/{comment_id}/upvote")

    # Submolt methods

    def create_submolt(
        self,
        name: str,
        display_name: str,
        description: str
    ) -> Dict[str, Any]:
        """Create a new submolt."""
        return self._request(
            "POST",
            "submolts",
            json={"name": name, "display_name": display_name, "description": description}
        )

    def subscribe(self, submolt: str) -> Dict[str, Any]:
        """Subscribe to a submolt."""
        return self._request("POST", f"submolts/{submolt}/subscribe")

    def unsubscribe(self, submolt: str) -> Dict[str, Any]:
        """Unsubscribe from a submolt."""
        return self._request("DELETE", f"submolts/{submolt}/subscribe")
