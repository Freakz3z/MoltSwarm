/**
 * Moltbook API client for MoltSwarm
 */

import axios, { AxiosInstance, AxiosRequestConfig } from "axios";
import { Post, Comment, ApiResponse } from "./types";

export class MoltbookClient {
  private client: AxiosInstance;
  private baseUrl: string;

  constructor(apiKey: string, baseUrl = "https://www.moltbook.com/api/v1") {
    this.baseUrl = baseUrl;
    this.client = axios.create({
      baseURL: baseUrl,
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
    });

    // Add retry logic for rate limiting
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 429) {
          const retryAfter = error.response.data?.retry_after_seconds || 60;
          console.log(`Rate limited. Waiting ${retryAfter}s...`);
          await new Promise((resolve) => setTimeout(resolve, retryAfter * 1000));
          return this.client.request(error.config);
        }
        return Promise.reject(error);
      }
    );
  }

  private async request<T>(config: AxiosRequestConfig): Promise<T> {
    const response = await this.client.request<ApiResponse<T>>(config);
    if (response.data.success) {
      return response.data.data as T;
    }
    throw new Error(response.data.error || "Request failed");
  }

  // Agent methods

  async getProfile(): Promise<any> {
    return this.request<any>({ method: "GET", url: "/agents/me" });
  }

  async updateProfile(description?: string): Promise<any> {
    return this.request<any>({
      method: "PATCH",
      url: "/agents/me",
      data: description ? { description } : {},
    });
  }

  // Post methods

  async createPost(
    submolt: string,
    title: string,
    content: string,
    url?: string
  ): Promise<{ post: Post }> {
    return this.request<{ post: Post }>({
      method: "POST",
      url: "/posts",
      data: { submolt, title, content, url },
    });
  }

  async getPost(postId: string): Promise<Post> {
    return this.request<Post>({ method: "GET", url: `/posts/${postId}` });
  }

  async getFeed(
    sort: "hot" | "new" | "top" | "rising" = "new",
    limit = 25,
    submolt?: string
  ): Promise<Post[]> {
    const params: any = { sort, limit };
    if (submolt) {
      params.submolt = submolt;
    }

    const response = await this.client.get<ApiResponse<{ posts: Post[] }>>(
      "/posts",
      { params }
    );
    return response.data.data?.posts || [];
  }

  async getPersonalizedFeed(
    sort: "hot" | "new" | "top" = "new",
    limit = 25
  ): Promise<Post[]> {
    const response = await this.client.get<ApiResponse<{ posts: Post[] }>>(
      "/feed",
      { params: { sort, limit } }
    );
    return response.data.data?.posts || [];
  }

  async searchPosts(
    query: string,
    type: "posts" | "comments" | "all" = "posts",
    limit = 20
  ): Promise<any[]> {
    const response = await this.client.get<ApiResponse<{ results: any[] }>>(
      "/search",
      { params: { q: query, type, limit } }
    );
    return response.data.data?.results || [];
  }

  // Comment methods

  async addComment(
    postId: string,
    content: string,
    parentId?: string
  ): Promise<{ comment: Comment }> {
    return this.request<{ comment: Comment }>({
      method: "POST",
      url: `/posts/${postId}/comments`,
      data: { content, parent_id: parentId },
    });
  }

  async getComments(
    postId: string,
    sort: "top" | "new" | "controversial" = "new"
  ): Promise<Comment[]> {
    const response = await this.client.get<ApiResponse<{ comments: Comment[] }>>(
      `/posts/${postId}/comments`,
      { params: { sort } }
    );
    return response.data.data?.comments || [];
  }

  // Voting methods

  async upvotePost(postId: string): Promise<any> {
    return this.request<any>({
      method: "POST",
      url: `/posts/${postId}/upvote`,
    });
  }

  async upvoteComment(commentId: string): Promise<any> {
    return this.request<any>({
      method: "POST",
      url: `/comments/${commentId}/upvote`,
    });
  }

  // Submolt methods

  async createSubmolt(
    name: string,
    displayName: string,
    description: string
  ): Promise<any> {
    return this.request<any>({
      method: "POST",
      url: "/submolts",
      data: { name, display_name: displayName, description },
    });
  }

  async subscribe(submolt: string): Promise<any> {
    return this.request<any>({
      method: "POST",
      url: `/submolts/${submolt}/subscribe`,
    });
  }

  async unsubscribe(submolt: string): Promise<any> {
    return this.request<any>({
      method: "DELETE",
      url: `/submolts/${submolt}/subscribe`,
    });
  }
}
