import {
    Article,
    ArticleStatus,
  } from "@/types/article";
  
  import { Edition } from "@/types/edition";
  
  const API_URL =
    process.env.NEXT_PUBLIC_API_URL ||
    "http://localhost:8000";
  
  async function request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const response = await fetch(
      `${API_URL}${endpoint}`,
      {
        ...options,
        headers: {
          "Content-Type": "application/json",
          ...options?.headers,
        },
      }
    );
  
    if (!response.ok) {
      const error = await response.text();
  
      throw new Error(
        error || `Request failed: ${response.status}`
      );
    }
  
    return response.json() as Promise<T>;
  }
  
  export const api = {
    getArticles: (
      status?: ArticleStatus
    ): Promise<Article[]> => {
      const query = status
        ? `?status=${encodeURIComponent(status)}`
        : "";
  
      return request<Article[]>(
        `/articles${query}`
      );
    },
  
    updateArticleStatus: (
      articleId: number,
      status: ArticleStatus
    ): Promise<Article> => {
      return request<Article>(
        `/articles/${articleId}/status`,
        {
          method: "PATCH",
          body: JSON.stringify({ status }),
        }
      );
    },
  
    getEditions: (): Promise<Edition[]> => {
      return request<Edition[]>("/editions");
    },
  
    createEdition: (
      title: string,
      description?: string
    ): Promise<Edition> => {
      return request<Edition>(
        "/editions",
        {
          method: "POST",
          body: JSON.stringify({
            title,
            description,
          }),
        }
      );
    },
  
    generateEdition: (
      editionId: number,
      limit = 8
    ): Promise<Edition> => {
      return request<Edition>(
        `/editions/${editionId}/generate?limit=${limit}`,
        {
          method: "POST",
        }
      );
    },
  
    publishEdition: (
      editionId: number
    ): Promise<Edition> => {
      return request<Edition>(
        `/editions/${editionId}/publish`,
        {
          method: "PATCH",
        }
      );
    },
  
    getEdition: (
      editionId: number
    ): Promise<Edition> => {
      return request<Edition>(
        `/editions/${editionId}`
      );
    },
  };