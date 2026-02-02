/**
 * Type definitions for MoltSwarm
 */

/** Moltbook API response wrapper */
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  hint?: string;
}

/** Moltbook post */
export interface Post {
  id: string;
  title: string;
  content: string;
  url?: string;
  author: Agent;
  submolt: Submolt;
  upvotes: number;
  downvotes: number;
  created_at: string;
}

/** Moltbook comment */
export interface Comment {
  id: string;
  content: string;
  author: Agent;
  post_id: string;
  parent_id?: string;
  upvotes: number;
  downvotes: number;
  created_at: string;
}

/** Moltbook agent */
export interface Agent {
  name: string;
  description?: string;
  karma?: number;
  follower_count?: number;
  following_count?: number;
}

/** Moltbook submolt (community) */
export interface Submolt {
  name: string;
  display_name: string;
  description?: string;
}

/** Swarm metadata in task */
export interface SwarmMetadata {
  version: string;
  job_id: string;
  type: string;
  skills: string[];
  reward_karma: boolean;
  claim_timeout: number;
  deadline?: string;
}

/** Task content */
export interface TaskContent {
  title: string;
  description: string;
  requirements: string[];
  output_format: string;
  validation: string;
}

/** Raw task data from post */
export interface RawTaskData {
  swarm: SwarmMetadata;
  task: TaskContent;
}

/** Skill handler function - receives Task object from protocols */
export type SkillHandler = (task: any) => string | Promise<string>;

/** Registered skill */
export interface Skill {
  name: string;
  handler: SkillHandler;
  description: string;
  tags: string[];
}

/** Node configuration */
export interface NodeConfig {
  name: string;
  description?: string;
  skills: string[];
  heartbeatInterval?: number;
  autoClaim?: boolean;
}

/** Moltbook client configuration */
export interface MoltbookConfig {
  apiKey: string;
  baseUrl?: string;
}

/** Complete swarm configuration */
export interface SwarmConfig {
  moltbook: MoltbookConfig;
  node: NodeConfig;
}
