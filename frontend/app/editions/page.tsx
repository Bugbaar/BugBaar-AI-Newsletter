"use client";

import { useEffect, useState } from "react";
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


export default function EditionsPage() {

  const [editions, setEditions] =
    useState<Edition[]>([]);

  const [title, setTitle] =
    useState("");

  const [description, setDescription] =
    useState("");


  async function loadEditions() {

    const data =
      await api.getEditions();

    setEditions(data);
  }


  useEffect(() => {
    loadEditions();
  }, []);


  async function createEdition() {

    if (!title.trim()) return;

    await api.createEdition(
      title,
      description
    );

    setTitle("");
    setDescription("");

    await loadEditions();
  }


  async function generateEdition(
    editionId: number
  ) {

    await api.generateEdition(
      editionId,
      8
    );

    await loadEditions();
  }


  async function publishEdition(
    editionId: number
  ) {

    await api.publishEdition(
      editionId
    );

    await loadEditions();
  }


  return (
    <main className="min-h-screen bg-gray-50">

      <div className="mx-auto max-w-6xl px-6 py-10">

        <h1 className="text-3xl font-bold">
          Newsletter Editions
        </h1>

        <p className="mt-2 text-gray-600">
          Build and publish curated newsletter editions.
        </p>


        <section className="mt-8 rounded-xl border bg-white p-6">

          <h2 className="text-lg font-semibold">
            Create edition
          </h2>


          <div className="mt-4 grid gap-3">

            <input
              value={title}
              onChange={(e) =>
                setTitle(e.target.value)
              }
              placeholder="Edition title"
              className="rounded-lg border px-4 py-3"
            />

            <textarea
              value={description}
              onChange={(e) =>
                setDescription(
                  e.target.value
                )
              }
              placeholder="Description"
              className="rounded-lg border px-4 py-3"
            />

            <button
              onClick={createEdition}
              className="w-fit rounded-lg bg-black px-5 py-3 text-sm text-white"
            >
              Create Edition
            </button>

          </div>

        </section>


        <section className="mt-8 space-y-5">

          {editions.map((edition) => (

            <article
              key={edition.id}
              className="rounded-xl border bg-white p-6"
            >

              <div className="flex items-center justify-between">

                <div>

                  <h2 className="text-xl font-semibold">
                    {edition.title}
                  </h2>

                  <p className="mt-1 text-sm text-gray-500">
                    {edition.description}
                  </p>

                </div>


                <span className="rounded-full bg-gray-100 px-3 py-1 text-sm">
                  {edition.status}
                </span>

              </div>


              <div className="mt-6">

                {edition.articles.length === 0 ? (

                  <p className="text-sm text-gray-500">
                    No articles selected yet.
                  </p>

                ) : (

                  <div className="space-y-3">

                    {edition.articles.map(
                      (article) => (

                        <div
                          key={article.article_id}
                          className="rounded-lg border p-4"
                        >

                          <div className="flex gap-4">

                            <span className="font-semibold">
                              {article.position}.
                            </span>

                            <div>

                              <h3 className="font-medium">
                                {article.title}
                              </h3>

                              <p className="mt-1 text-sm text-gray-500">
                                {article.category}
                                {" · "}
                                Score:{" "}
                                {article.relevance_score}
                              </p>

                            </div>

                          </div>

                        </div>

                      )
                    )}

                  </div>

                )}

              </div>


              {edition.status === "DRAFT" && (

                <div className="mt-6 flex gap-3">

                  <button
                    onClick={() =>
                      generateEdition(
                        edition.id
                      )
                    }
                    className="rounded-lg bg-black px-4 py-2 text-sm text-white"
                  >
                    Generate top articles
                  </button>


                  {edition.articles.length > 0 && (

                    <button
                      onClick={() =>
                        publishEdition(
                          edition.id
                        )
                      }
                      className="rounded-lg border px-4 py-2 text-sm"
                    >
                      Publish
                    </button>

                  )}

                </div>

              )}

            </article>

          ))}

        </section>

      </div>

    </main>
  );
}