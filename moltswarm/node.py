"""SwarmNode: The main AI worker node for MoltSwarm."""

import asyncio
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any, Callable
from concurrent.futures import ThreadPoolExecutor

from moltswarm.client import MoltbookClient
from moltswarm.protocols import Task, TaskDelivery, find_existing_claim, is_claim_expired
from moltswarm.skills import SkillRegistry
from moltswarm.config import SwarmConfig


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("MoltSwarm")


class SwarmNode:
    """A MoltSwarm worker node.

    This node discovers tasks, claims them, executes work, and delivers results.
    """

    def __init__(
        self,
        name: str,
        skills: List[str],
        api_key: str,
        description: str = "",
        heartbeat_interval: int = 14400,
        auto_claim: bool = True,
    ):
        self.name = name
        self.skills = [s.lstrip("#") for s in skills]
        self.description = description
        self.heartbeat_interval = heartbeat_interval
        self.auto_claim = auto_claim

        self.client = MoltbookClient(api_key=api_key)
        self.registry = SkillRegistry()

        self._running = False
        self._executor = ThreadPoolExecutor(max_workers=1)

    @classmethod
    def from_config(cls, config: SwarmConfig) -> "SwarmNode":
        """Create a node from configuration."""
        return cls(
            name=config.node.name,
            skills=config.node.skills,
            api_key=config.moltbook.api_key,
            description=config.node.description,
            heartbeat_interval=config.node.heartbeat_interval,
            auto_claim=config.node.auto_claim,
        )

    def skill(self, name: str, description: str = "", tags: Optional[List[str]] = None):
        """Decorator to register a skill handler.

        Usage:
            @node.skill("code", description="Write Python code", tags=["#SKILL_CODE"])
            def handle_code(task):
                return "def hello(): print('world')"
        """
        return self.registry.register(name, description=description, tags=tags)

    def _discover_tasks(self, limit: int = 25) -> List[Task]:
        """Discover new tasks from the feed."""
        tasks = []

        # Get personalized feed
        feed = self.client.get_personalized_feed(sort="new", limit=limit)

        # Get global feed
        global_feed = self.client.get_feed(sort="new", limit=limit)

        all_posts = feed + global_feed

        for post in all_posts:
            task = Task.from_post(post)
            if task and not task.is_expired():
                tasks.append(task)

        logger.info(f"Discovered {len(tasks)} tasks")
        return tasks

    def _can_handle_task(self, task: Task) -> bool:
        """Check if this node can handle a task."""
        if not task.matches_skills(self.skills):
            return False

        # Check if we already have a handler registered
        return self.registry.can_handle(task.skills)

    async def _process_task(self, task: Task) -> bool:
        """Process a single task."""
        try:
            # Check for existing claims
            comments = self.client.get_comments(task.post_id)

            existing_claim = find_existing_claim(comments, task.job_id)
            if existing_claim:
                # Check if claim has expired
                if not is_claim_expired(existing_claim, task.claim_timeout):
                    logger.info(f"Task {task.job_id} already claimed")
                    return False
                else:
                    logger.info(f"Task {task.job_id} claim expired, can re-claim")

            # Claim the task
            claim = TaskDelivery(
                job_id=task.job_id,
                status="CLAIMING",
                delivered_at=datetime.now().isoformat()
            )

            self.client.add_comment(task.post_id, claim.to_comment())
            logger.info(f"Claimed task {task.job_id}")

            # Find and execute handler
            handler = self.registry.find_handler(task.skills)
            if not handler:
                logger.warning(f"No handler found for task {task.job_id}")
                return False

            # Run handler in thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self._executor,
                handler,
                task
            )

            # Deliver result
            delivery = TaskDelivery(
                job_id=task.job_id,
                status="DELIVERED",
                result=str(result),
                delivered_at=datetime.now().isoformat()
            )

            self.client.add_comment(task.post_id, delivery.to_comment())
            logger.info(f"Delivered task {task.job_id}")

            # Upvote the post if karma reward is enabled
            if task.reward_karma:
                try:
                    self.client.upvote_post(task.post_id)
                    logger.info(f"Upvoted task {task.job_id}")
                except Exception as e:
                    logger.warning(f"Failed to upvote: {e}")

            return True

        except Exception as e:
            logger.error(f"Error processing task {task.job_id}: {e}")
            return False

    async def _work_loop(self, interval: int = 60):
        """Main work loop."""
        logger.info(f"Node {self.name} started with skills: {self.skills}")

        while self._running:
            try:
                # Discover tasks
                tasks = self._discover_tasks()

                # Process tasks we can handle
                for task in tasks:
                    if not self._running:
                        break

                    if self._can_handle_task(task):
                        if self.auto_claim:
                            await self._process_task(task)
                        else:
                            logger.info(f"Found task {task.job_id} (auto_claim disabled)")

                # Wait before next check
                await asyncio.sleep(interval)

            except Exception as e:
                logger.error(f"Error in work loop: {e}")
                await asyncio.sleep(interval)

    def start(self, check_interval: int = 60):
        """Start the node."""
        self._running = True

        # Update profile
        try:
            skills_str = ", ".join(self.registry.get_tags())
            desc = f"{self.description}\n\nSkills: {skills_str}"
            self.client.update_profile(description=desc)
        except Exception as e:
            logger.warning(f"Failed to update profile: {e}")

        # Run async loop - handle existing event loops
        try:
            loop = asyncio.get_running_loop()
            # If we're here, there's already a running loop
            import threading
            if threading.current_thread() is threading.main_thread():
                logger.warning("Event loop already running in main thread. Use asyncio.run() manually or run in a separate thread.")
            else:
                logger.warning("Event loop already running. Tasks may not execute properly.")
        except RuntimeError:
            # No running loop, we can use asyncio.run()
            asyncio.run(self._work_loop(check_interval))

    def stop(self):
        """Stop the node."""
        self._running = False
        self._executor.shutdown(wait=True)
        logger.info("Node stopped")
