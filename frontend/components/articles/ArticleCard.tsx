"use client";

import { Article } from "@/types/article";

interface ArticleCardProps {
  article: Article;
  onStatusChange: (
    articleId: number,
    status: string
  ) => void;
}


export default function ArticleCard({
  article,
  onStatusChange,
}: ArticleCardProps) {

  return (
    <article className="rounded-xl border bg-white p-5 shadow-sm">

      <div className="mb-3 flex items-start justify-between gap-4">

        <div>
          <p className="text-sm font-medium text-gray-500">
            {article.source}
          </p>

          <h2 className="mt-1 text-lg font-semibold text-gray-900">
            {article.title}
          </h2>
        </div>

        <span className="rounded-full bg-gray-100 px-3 py-1 text-sm">
          {article.category || "Uncategorized"}
        </span>

      </div>


      {article.summary && (
        <p className="text-sm leading-6 text-gray-600">
          {article.summary}
        </p>
      )}


      {article.key_takeaways &&
        article.key_takeaways.length > 0 && (

        <div className="mt-4">

          <h3 className="text-sm font-semibold">
            Key takeaways
          </h3>

          <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-gray-600">

            {article.key_takeaways.map(
              (takeaway, index) => (
                <li key={index}>
                  {takeaway}
                </li>
              )
            )}

          </ul>

        </div>
      )}


      <div className="mt-5 flex items-center justify-between">

        <div>
          <span className="text-sm text-gray-500">
            Relevance
          </span>

          <span className="ml-2 font-semibold">
            {article.relevance_score ?? "—"}
          </span>
        </div>


        <div className="flex gap-2">

          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-lg border px-3 py-2 text-sm"
          >
            Read
          </a>

          {article.status !== "APPROVED" && (
            <button
              onClick={() =>
                onStatusChange(
                  article.id,
                  "APPROVED"
                )
              }
              className="rounded-lg bg-black px-3 py-2 text-sm text-white"
            >
              Approve
            </button>
          )}

          {article.status !== "REJECTED" && (
            <button
              onClick={() =>
                onStatusChange(
                  article.id,
                  "REJECTED"
                )
              }
              className="rounded-lg border px-3 py-2 text-sm"
            >
              Reject
            </button>
          )}

        </div>

      </div>

    </article>
  );
}