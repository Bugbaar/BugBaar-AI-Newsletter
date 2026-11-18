"use client";

import { useEffect, useState } from "react";

import ArticleCard from "@/components/articles/ArticleCard";
import { api } from "@/lib/api";
import { Article } from "@/types/article";


export default function ArticlesPage() {

  const [articles, setArticles] =
    useState<Article[]>([]);

  const [status, setStatus] =
    useState("PENDING");

  const [loading, setLoading] =
    useState(true);


  async function loadArticles() {

    try {
      setLoading(true);

      const data =
        await api.getArticles(status);

      setArticles(data);

    } catch (error) {

      console.error(
        "Failed to load articles:",
        error
      );

    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    loadArticles();
  }, [status]);


  async function handleStatusChange(
    articleId: number,
    newStatus: string
  ) {

    try {

      await api.updateArticleStatus(
        articleId,
        newStatus
      );

      await loadArticles();

    } catch (error) {

      console.error(
        "Failed to update article:",
        error
      );

    }
  }


  return (
    <main className="min-h-screen bg-gray-50">

      <div className="mx-auto max-w-6xl px-6 py-10">

        <div className="mb-8">

          <h1 className="text-3xl font-bold">
            Article Review
          </h1>

          <p className="mt-2 text-gray-600">
            Review AI-curated technology stories
            before publishing.
          </p>

        </div>


        <div className="mb-6 flex gap-2">

          {[
            "PENDING",
            "APPROVED",
            "REJECTED",
          ].map((value) => (

            <button
              key={value}
              onClick={() => setStatus(value)}
              className={`rounded-lg px-4 py-2 text-sm ${
                status === value
                  ? "bg-black text-white"
                  : "border bg-white"
              }`}
            >
              {value}
            </button>

          ))}

        </div>


        {loading ? (

          <p className="text-gray-500">
            Loading articles...
          </p>

        ) : articles.length === 0 ? (

          <div className="rounded-xl border bg-white p-10 text-center">
            <p className="text-gray-500">
              No {status.toLowerCase()} articles.
            </p>
          </div>

        ) : (

          <div className="grid gap-5">

            {articles.map((article) => (

              <ArticleCard
                key={article.id}
                article={article}
                onStatusChange={
                  handleStatusChange
                }
              />

            ))}

          </div>

        )}

      </div>

    </main>
  );
}