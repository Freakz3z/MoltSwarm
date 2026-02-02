/**
 * Skill management system for MoltSwarm
 */

import { Skill, SkillHandler } from "./types";

/**
 * Registry for managing agent skills
 */
export class SkillRegistry {
  private skills: Map<string, Skill> = new Map();

  /**
   * Register a skill handler
   */
  register(
    name: string,
    handler: SkillHandler,
    description = "",
    tags?: string[]
  ): void {
    const skillTags = tags || [`#SKILL_${name.toUpperCase()}`];
    this.skills.set(name, {
      name,
      handler,
      description,
      tags: skillTags,
    });
  }

  /**
   * Get a skill by name
   */
  get(name: string): Skill | undefined {
    return this.skills.get(name);
  }

  /**
   * Get all registered skills
   */
  getAll(): Map<string, Skill> {
    return new Map(this.skills);
  }

  /**
   * Get all skill tags
   */
  getTags(): string[] {
    const tags: string[] = [];
    for (const skill of this.skills.values()) {
      tags.push(...skill.tags);
    }
    return Array.from(new Set(tags));
  }

  /**
   * Check if registry can handle a task with required skills
   */
  canHandle(taskSkills: string[]): boolean {
    const myTags = this.getTags();
    const myTagsNormalized = myTags.map((t) => t.replace("#", "").toLowerCase());
    const taskNormalized = taskSkills.map((t) => t.replace("#", "").toLowerCase());

    return taskNormalized.some((req) => myTagsNormalized.includes(req));
  }

  /**
   * Find the best handler for a task based on skills
   */
  findHandler(taskSkills: string[]): SkillHandler | undefined {
    for (const skill of this.skills.values()) {
      for (const tag of skill.tags) {
        const tagNormalized = tag.replace("#", "").toLowerCase();
        if (
          taskSkills.some((ts) => ts.replace("#", "").toLowerCase() === tagNormalized)
        ) {
          return skill.handler;
        }
      }
    }
    return undefined;
  }
}
