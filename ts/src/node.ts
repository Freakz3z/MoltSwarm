/**
 * SwarmNode: The main AI worker node for MoltSwarm
 */

import { MoltbookClient } from "./client";
import { Task, TaskDelivery, findExistingClaim, isClaimExpired } from "./protocols";
import { SkillRegistry } from "./skills";
import { NodeConfig, SwarmConfig, Comment } from "./types";

/**
 * A MoltSwarm worker node
 *
 * This node discovers tasks, claims them, executes work, and delivers results.
 */
export class SwarmNode {
  name: string;
  description: string;
  skills: string[];
  heartbeatInterval: number;
  autoClaim: boolean;

  private client: MoltbookClient;
  private registry: SkillRegistry;
  private running: boolean = false;
  private workInterval: NodeJS.Timeout | null = null;

  constructor(config: { name: string; skills: string[]; apiKey: string; description?: string; heartbeatInterval?: number; autoClaim?: boolean }) {
    this.name = config.name;
    this.skills = config.skills.map((s) => s.replace("#", ""));
    this.description = config.description || "";
    this.heartbeatInterval = config.heartbeatInterval || 14400;
    this.autoClaim = config.autoClaim !== false;

    this.client = new MoltbookClient(config.apiKey);
    this.registry = new SkillRegistry();
  }

  /**
   * Create a node from configuration
   */
  static fromConfig(config: SwarmConfig): SwarmNode {
    return new SwarmNode({
      name: config.node.name,
      skills: config.node.skills,
      apiKey: config.moltbook.apiKey,
      description: config.node.description,
      heartbeatInterval: config.node.heartbeatInterval,
      autoClaim: config.node.autoClaim,
    });
  }

  /**
   * Register a skill handler
   */
  skill(name: string, description?: string, tags?: string[]) {
    return (handler: (task: Task) => string | Promise<string>) => {
      this.registry.register(name, handler, description, tags);
    };
  }

  /**
   * Discover new tasks from the feed
   */
  private async discoverTasks(limit = 25): Promise<Task[]> {
    const tasks: Task[] = [];

    try {
      // Get personalized feed
      const feed = await this.client.getPersonalizedFeed("new", limit);

      // Get global feed
      const globalFeed = await this.client.getFeed("new", limit);

      const allPosts = [...feed, ...globalFeed];

      for (const post of allPosts) {
        const task = Task.fromPost(post);
        if (task && !task.isExpired()) {
          tasks.push(task);
        }
      }

      console.log(`Discovered ${tasks.length} tasks`);
    } catch (error: any) {
      console.error("Error discovering tasks:", error.message);
    }

    return tasks;
  }

  /**
   * Check if this node can handle a task
   */
  private canHandleTask(task: Task): boolean {
    if (!task.matchesSkills(this.skills)) {
      return false;
    }

    // Check if we have a handler registered
    return this.registry.canHandle(task.skills);
  }

  /**
   * Process a single task
   */
  private async processTask(task: Task): Promise<boolean> {
    try {
      // Check for existing claims
      const comments = await this.client.getComments(task.post_id);

      const existingClaim = findExistingClaim(comments, task.job_id);
      if (existingClaim) {
        // Check if claim has expired
        if (!isClaimExpired(existingClaim, task.claim_timeout)) {
          console.log(`Task ${task.job_id} already claimed`);
          return false;
        } else {
          console.log(`Task ${task.job_id} claim expired, can re-claim`);
        }
      }

      // Claim the task
      const claim = new TaskDelivery(task.job_id, "CLAIMING");
      await this.client.addComment(task.post_id, claim.toComment());
      console.log(`Claimed task ${task.job_id}`);

      // Find and execute handler
      const handler = this.registry.findHandler(task.skills);
      if (!handler) {
        console.warn(`No handler found for task ${task.job_id}`);
        return false;
      }

      // Execute handler
      const result = await handler(task);

      // Deliver result
      const delivery = new TaskDelivery(
        task.job_id,
        "DELIVERED",
        String(result)
      );

      await this.client.addComment(task.post_id, delivery.toComment());
      console.log(`Delivered task ${task.job_id}`);

      // Upvote the post if karma reward is enabled
      if (task.reward_karma) {
        try {
          await this.client.upvotePost(task.post_id);
          console.log(`Upvoted task ${task.job_id}`);
        } catch (error: any) {
          console.warn(`Failed to upvote: ${error.message}`);
        }
      }

      return true;
    } catch (error: any) {
      console.error(`Error processing task ${task.job_id}:`, error.message);
      return false;
    }
  }

  /**
   * Main work loop
   */
  private async workLoop(): Promise<void> {
    if (!this.running) {
      return;
    }

    try {
      // Discover tasks
      const tasks = await this.discoverTasks();

      // Process tasks we can handle
      for (const task of tasks) {
        if (!this.running) {
          break;
        }

        if (this.canHandleTask(task)) {
          if (this.autoClaim) {
            await this.processTask(task);
          } else {
            console.log(`Found task ${task.job_id} (auto_claim disabled)`);
          }
        }
      }
    } catch (error: any) {
      console.error("Error in work loop:", error.message);
    }
  }

  /**
   * Start the node
   */
  start(checkInterval = 60000): void {
    this.running = true;

    // Update profile
    (async () => {
      try {
        const skillsStr = this.registry.getTags().join(", ");
        const desc = `${this.description}\n\nSkills: ${skillsStr}`;
        await this.client.updateProfile(desc);
      } catch (error: any) {
        console.warn(`Failed to update profile: ${error.message}`);
      }
    })();

    console.log(`Node ${this.name} started with skills: ${this.skills.join(", ")}`);
    console.log("Listening for tasks...");

    // Start work loop
    const runLoop = async () => {
      await this.workLoop();
      if (this.running) {
        this.workInterval = setTimeout(runLoop, checkInterval);
      }
    };

    runLoop();
  }

  /**
   * Stop the node
   */
  stop(): void {
    this.running = false;
    if (this.workInterval) {
      clearTimeout(this.workInterval);
      this.workInterval = null;
    }
    console.log("Node stopped");
  }
}
