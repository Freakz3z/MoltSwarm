/**
 * Configuration management for MoltSwarm
 */

import { existsSync, readFileSync } from "fs";
import { resolve } from "path";
import * as yaml from "js-yaml";
import { SwarmConfig, NodeConfig, MoltbookConfig } from "./types";

/**
 * Load Moltbook configuration
 */
export class MoltbookConfigClass implements MoltbookConfig {
  apiKey: string;
  baseUrl: string;

  constructor(config: MoltbookConfig) {
    this.apiKey = config.apiKey;
    this.baseUrl = config.baseUrl || "https://www.moltbook.com/api/v1";
  }
}

/**
 * Load Swarm configuration from file or environment
 */
export function loadConfig(configPath?: string): SwarmConfig {
  // Try loading from file first
  if (configPath) {
    return loadConfigFromFile(configPath);
  }

  // Try default config paths
  const defaultPaths = [
    "config.yaml",
    "config.yml",
    resolve(process.env.HOME || "", ".config", "moltswarm", "config.yaml"),
  ];

  for (const path of defaultPaths) {
    if (existsSync(path)) {
      return loadConfigFromFile(path);
    }
  }

  // Fall back to environment variables
  return loadConfigFromEnv();
}

/**
 * Load configuration from a YAML file
 */
export function loadConfigFromFile(path: string): SwarmConfig {
  const fileContent = readFileSync(path, "utf8");
  const data = yaml.load(fileContent) as any;

  return {
    moltbook: {
      apiKey: data.moltbook.api_key,
      baseUrl: data.moltbook.base_url || "https://www.moltbook.com/api/v1",
    },
    node: {
      name: data.swarm_node.name,
      description: data.swarm_node.description || "",
      skills: data.swarm_node.skills || [],
      heartbeatInterval: data.swarm_node.heartbeat_interval || 14400,
      autoClaim: data.swarm_node.auto_claim !== false,
    },
  };
}

/**
 * Load configuration from environment variables
 */
export function loadConfigFromEnv(): SwarmConfig {
  const apiKey = process.env.MOLTBOOK_API_KEY;
  if (!apiKey) {
    throw new Error("MOLTBOOK_API_KEY environment variable not set");
  }

  return {
    moltbook: {
      apiKey,
      baseUrl: process.env.MOLTBOOK_BASE_URL || "https://www.moltbook.com/api/v1",
    },
    node: {
      name: process.env.SWARM_NODE_NAME || "AIWorker",
      description: process.env.SWARM_NODE_DESC || "",
      skills: process.env.SWARM_NODE_SKILLS?.split(",") || [],
      heartbeatInterval: parseInt(process.env.SWARM_HEARTBEAT_INTERVAL || "14400"),
      autoClaim: process.env.SWARM_AUTO_CLAIM !== "false",
    },
  };
}
