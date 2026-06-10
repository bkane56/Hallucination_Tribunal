"use client";

import { useCallback, useEffect, useState } from "react";
import { api } from "@/lib/api/client";
import type { Document } from "@/lib/types";
import { SampleGovernancePanel } from "./SampleGovernancePanel";
import { UploadPanel } from "./UploadPanel";

export function CorpusManager() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const loadDocuments = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.listDocuments();
      setDocuments(data.documents);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load documents");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDocuments();
  }, [loadDocuments]);

  async function handleDelete(id: string) {
    await api.deleteDocument(id);
    await loadDocuments();
  }

  async function handleRebuild() {
    await api.rebuildIndex();
    await loadDocuments();
  }

  return (
    <div className="space-y-6">
      <SampleGovernancePanel onImported={loadDocuments} />
      <UploadPanel onUploaded={loadDocuments} />
      <div className="rounded-lg border border-paper-line bg-ivory p-6 shadow-sm">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold">Document Corpus</h2>
          <button
            type="button"
            onClick={handleRebuild}
            className="rounded-md border border-paper-line px-3 py-1.5 text-sm hover:bg-parchment"
          >
            Rebuild Index
          </button>
        </div>
        {loading && <p className="text-sm text-slate-gray">Loading...</p>}
        {error && (
          <p className="text-sm text-overruled-red" role="alert">
            {error}
          </p>
        )}
        {!loading && documents.length === 0 && (
          <p className="text-sm text-slate-gray">No documents uploaded yet.</p>
        )}
        {documents.length > 0 && (
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead>
                <tr className="border-b border-paper-line text-slate-gray">
                  <th className="px-2 py-2">Filename</th>
                  <th className="px-2 py-2">Type</th>
                  <th className="px-2 py-2">Chunks</th>
                  <th className="px-2 py-2">Status</th>
                  <th className="px-2 py-2">Actions</th>
                </tr>
              </thead>
              <tbody>
                {documents.map((doc) => (
                  <tr key={doc.document_id} className="border-b border-paper-line/60">
                    <td className="px-2 py-2">{doc.filename}</td>
                    <td className="px-2 py-2">{doc.file_type}</td>
                    <td className="px-2 py-2">{doc.chunk_count}</td>
                    <td className="px-2 py-2">
                      {doc.status}
                      {doc.error_message && (
                        <span className="block text-overruled-red">{doc.error_message}</span>
                      )}
                    </td>
                    <td className="px-2 py-2">
                      <button
                        type="button"
                        onClick={() => handleDelete(doc.document_id)}
                        className="text-overruled-red hover:underline"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
