"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";

interface EditionArticle {
  position: number;
  article_id: number;
  title: string;
  summary: string | null;
  category: string | null;
  relevance_score: number | null;
  url: string;
}

interface Edition {
  id: number;
  title: string;
  description: string | null;
  status: string;
  published_at: string | null;
  articles: EditionArticle[];
}

export default function NewsletterPage() {
  const params = useParams();
  const id = Number(params.id);

  const [edition, setEdition] = useState<Edition | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadEdition() {
      try {
        const data = await api.getEdition(id);
        setEdition(data);
      } catch (err) {
        console.error(err);
        setError("Newsletter could not be loaded.");
      } finally {
        setLoading(false);
      }
    }

    if (id) {
      loadEdition();
    }
  }, [id]);

  if (loading) {
    return (
      <main className="min-h-screen bg-gray-50 px-6 py-20">
        <div className="mx-auto max-w-4xl text-center">
          <p className="text-gray-500">Loading newsletter...</p>
        </div>
      </main>
    );
  }

  if (error || !edition) {
    return (
      <main className="min-h-screen bg-gray-50 px-6 py-20">
        <div className="mx-auto max-w-4xl rounded-2xl border bg-white p-10 text-center">
          <h1 className="text-2xl font-bold">
            Newsletter unavailable
          </h1>
          <p className="mt-3 text-gray-500">
            {error || "This newsletter does not exist."}
          </p>
        </div>
      </main>
    );
  }

  if (edition.status !== "PUBLISHED") {
    return (
      <main className="min-h-screen bg-gray-50 px-6 py-20">
        <div className="mx-auto max-w-4xl rounded-2xl border bg-white p-10 text-center">
          <p className="text-sm font-medium uppercase tracking-wide text-gray-400">
            BugBaar AI Newsletter
          </p>

          <h1 className="mt-3 text-2xl font-bold">
            Newsletter not published
          </h1>

          <p className="mt-3 text-gray-500">
            This edition is still being prepared by the editorial team.
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-100">
      <div className="mx-auto max-w-4xl px-5 py-10 sm:px-8">
        {/* Header */}
        <header className="rounded-2xl bg-black px-7 py-10 text-white shadow-sm">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-gray-400">
            BugBaar AI Newsletter
          </p>

          <h1 className="mt-4 text-4xl font-bold tracking-tight sm:text-5xl">
            {edition.title}
          </h1>

          {edition.description && (
            <p className="mt-5 max-w-2xl text-lg leading-8 text-gray-300">
              {edition.description}
            </p>
          )}

          {edition.published_at && (
            <p className="mt-6 text-sm text-gray-400">
              Published{" "}
              {new Date(edition.published_at).toLocaleDateString()}
            </p>
          )}
        </header>

        {/* Articles */}
        <section className="mt-8 space-y-6">
          {edition.articles.map((article) => (
            <article
              key={article.article_id}
              className="rounded-2xl border bg-white p-7 shadow-sm"
            >
              <div className="flex items-start gap-4">
                <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-gray-100 text-sm font-bold">
                  {article.position}
                </span>

                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    {article.category && (
                      <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-semibold">
                        {article.category}
                      </span>
                    )}

                    <span className="text-xs text-gray-400">
                      {article.title}
                    </span>
                  </div>

                  <h2 className="mt-3 text-2xl font-bold leading-tight text-gray-900">
                    {article.title}
                  </h2>

                  {article.summary && (
                    <p className="mt-4 text-base leading-7 text-gray-600">
                      {article.summary}
                    </p>
                  )}

                  <div className="mt-6">
                    <a
                      href={article.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex rounded-lg bg-black px-4 py-2.5 text-sm font-medium text-white transition hover:bg-gray-800"
                    >
                      Read original →
                    </a>
                  </div>
                </div>
              </div>
            </article>
          ))}
        </section>

        {/* Footer */}
        <footer className="py-10 text-center">
          <p className="text-sm text-gray-400">
            Curated with AI. Reviewed by humans.
          </p>
          <p className="mt-2 text-xs text-gray-400">
            BugBaar AI Newsletter
          </p>
        </footer>
      </div>
    </main>
  );
}