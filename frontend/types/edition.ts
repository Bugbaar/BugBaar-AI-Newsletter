export interface EditionArticle {
    position: number;
    article_id: number;
    title: string;
    summary: string | null;
    category: string | null;
    relevance_score: number | null;
    url: string;
  }
  
  export interface Edition {
    id: number;
    title: string;
    description: string | null;
    status: "DRAFT" | "PUBLISHED";
    published_at: string | null;
    articles: EditionArticle[];
  }
  
  export interface EditionCreateResponse extends Edition {}
  
  export interface EditionGenerateResponse extends Edition {}
  
  export interface EditionPublishResponse extends Edition {}