export type ArticleStatus =
  | "PENDING"
  | "PROCESSING"
  | "APPROVED"
  | "REJECTED";

export type ArticleCategory =
  | "AI"
  | "Engineering"
  | "Startups"
  | "Careers"
  | "Open Source"
  | "Research"
  | "Other";

export interface Article {
  id: number;
  title: string;
  url: string;
  source: string;
  content: string | null;
  summary: string | null;
  category: ArticleCategory | null;
  key_takeaways: string[] | null;
  relevance_score: number | null;
  status: ArticleStatus;
  published_at: string | null;
}