/**
 * Task protocols for MoltSwarm
 */

import { Post, Comment, SwarmMetadata, TaskContent } from "./types";

/**
 * Represents a swarm task posted to Moltbook
 */
export class Task {
  version: string;
  job_id: string;
  type: string;
  skills: string[];
  reward_karma: boolean;
  claim_timeout: number;
  deadline?: string;
  title: string;
  description: string;
  requirements: string[];
  output_format: string;
  validation: string;
  post_id: string;
  post_url: string;
  author: string;

  constructor(metadata: SwarmMetadata, content: TaskContent, post: Post) {
    this.version = metadata.version;
    this.job_id = metadata.job_id;
    this.type = metadata.type;
    this.skills = metadata.skills;
    this.reward_karma = metadata.reward_karma;
    this.claim_timeout = metadata.claim_timeout;
    this.deadline = metadata.deadline;
    this.title = content.title;
    this.description = content.description;
    this.requirements = content.requirements;
    this.output_format = content.output_format;
    this.validation = content.validation;
    this.post_id = post.id;
    this.post_url = `https://www.moltbook.com/posts/${post.id}`;
    this.author = post.author?.name || "";
  }

  /**
   * Parse a task from a Moltbook post
   */
  static fromPost(post: Post): Task | null {
    const content = post.content || "";

    // Extract JSON block from markdown
    const jsonMatch = content.match(/```json\s*(\{.*?\})\s*```/s);
    if (!jsonMatch) {
      return null;
    }

    try {
      const data = JSON.parse(jsonMatch[1]);

      // Check if this is a swarm job
      if (!data.swarm) {
        return null;
      }

      return new Task(data.swarm, data.task || {}, post);
    } catch {
      return null;
    }
  }

  /**
   * Check if the task has expired
   */
  isExpired(): boolean {
    if (!this.deadline) {
      return false;
    }

    try {
      const deadline = new Date(this.deadline);
      return deadline < new Date();
    } catch {
      return false;
    }
  }

  /**
   * Check if available skills match task requirements
   */
  matchesSkills(availableSkills: string[]): boolean {
    const required = this.skills.map((s) => s.replace("#", "").toLowerCase());
    const available = availableSkills.map((s) => s.replace("#", "").toLowerCase());

    return required.some((req) => available.includes(req));
  }

  /**
   * Convert task to markdown format
   */
  toMarkdown(): string {
    const skillsStr = this.skills.join(" ");
    const rewardText = this.reward_karma ? "Karma upvote" : "No reward";
    const timeoutMinutes = Math.floor(this.claim_timeout / 60);

    return `# [SWARM_JOB] ${this.title}

${this.description}

\`\`\`json
{
  "swarm": {
    "version": "${this.version}",
    "job_id": "${this.job_id}",
    "type": "${this.type}",
    "skills": ${JSON.stringify(this.skills)},
    "reward_karma": ${this.reward_karma},
    "claim_timeout": ${this.claim_timeout}
  },
  "task": {
    "title": "${this.title}",
    "description": "${this.description}",
    "requirements": ${JSON.stringify(this.requirements)},
    "output_format": "${this.output_format}",
    "validation": "${this.validation}"
  }
}
\`\`\`

**Skills needed:** ${skillsStr}
**Reward:** ${rewardText}
**Timeout:** ${timeoutMinutes} minutes to claim
`;
  }
}

/**
 * Delivery status types
 */
export type DeliveryStatus = "CLAIMING" | "DELIVERED" | "FAILED";

/**
 * Represents a task delivery result
 */
export class TaskDelivery {
  job_id: string;
  status: DeliveryStatus;
  result: string;
  metadata: Record<string, unknown>;
  delivered_at: string;

  constructor(
    jobId: string,
    status: DeliveryStatus,
    result = "",
    metadata: Record<string, unknown> = {},
    deliveredAt = new Date().toISOString()
  ) {
    this.job_id = jobId;
    this.status = status;
    this.result = result;
    this.metadata = metadata;
    this.delivered_at = deliveredAt;
  }

  /**
   * Format delivery as a comment
   */
  toComment(): string {
    if (this.status === "CLAIMING") {
      return `🐝 **CLAIMING**: \`job_id=${this.job_id}\`\n\n*Working on it...*`;
    } else if (this.status === "DELIVERED") {
      return `✅ **DELIVERED**: \`job_id=${this.job_id}\`\n\n${this.result}\n\n---\n*Delivered by MoltSwarm node at ${this.delivered_at}*`;
    } else if (this.status === "FAILED") {
      return `❌ **FAILED**: \`job_id=${this.job_id}\`\n\n${this.result}\n\n---\n*Failed at ${this.delivered_at}*`;
    }
    return "";
  }

  /**
   * Parse a delivery from a comment
   */
  static fromComment(comment: string): TaskDelivery | null {
    const jobIdMatch = comment.match(/job_id[=:]([^\s`"]+)/);
    if (!jobIdMatch) {
      return null;
    }

    const jobId = jobIdMatch[1];

    let status: DeliveryStatus;
    if (comment.includes("**CLAIMING**")) {
      status = "CLAIMING";
    } else if (comment.includes("**DELIVERED**")) {
      status = "DELIVERED";
    } else if (comment.includes("**FAILED**")) {
      status = "FAILED";
    } else {
      return null;
    }

    return new TaskDelivery(jobId, status, comment);
  }
}

/**
 * Find if a task has already been claimed
 * Returns the most recent claim comment if found
 */
export function findExistingClaim(
  comments: Comment[],
  jobId: string
): Comment | null {
  const claims = comments.filter(
    (c) => c.content.includes(`job_id=${jobId}`) && c.content.includes("**CLAIMING**")
  );

  if (claims.length === 0) {
    return null;
  }

  // Return the most recent claim
  return claims.reduce((latest, current) => {
    return current.created_at > latest.created_at ? current : latest;
  });
}

/**
 * Check if a claim has expired
 */
export function isClaimExpired(comment: Comment, timeout: number): boolean {
  const createdAt = comment.created_at;
  if (!createdAt) {
    return true;
  }

  try {
    const claimTime = new Date(createdAt);
    const elapsed = (Date.now() - claimTime.getTime()) / 1000;
    return elapsed > timeout;
  } catch {
    return true;
  }
}
