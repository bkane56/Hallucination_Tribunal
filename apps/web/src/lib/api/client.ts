const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${BACKEND_URL}${path}`, options);
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(error.detail || "Request failed");
  }
  return response.json();
}

export const api = {
  health: () => request<{ status: string; version: string }>("/health"),

  listDocuments: () =>
    request<{ documents: import("./types").Document[] }>("/documents"),

  uploadDocument: async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return request<{ document_id: string; filename: string; status: string; chunk_count: number }>(
      "/documents/upload",
      { method: "POST", body: formData }
    );
  },

  listSampleDocuments: () =>
    request<{ samples: import("./types").SampleDocument[]; categories: string[] }>(
      "/documents/samples"
    ),

  importSampleDocuments: (sampleIds: string[]) =>
    request<{
      imported: import("./types").SampleDocumentImportResult[];
      skipped: import("./types").SampleDocumentImportResult[];
      errors: import("./types").SampleDocumentImportResult[];
    }>("/documents/samples/import", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sample_ids: sampleIds }),
    }),

  deleteDocument: (id: string) =>
    request<{ status: string; document_id: string }>(`/documents/${id}`, {
      method: "DELETE",
    }),

  rebuildIndex: () =>
    request<{ rebuilt_count: number; total_documents: number }>(
      "/documents/rebuild-index",
      { method: "POST" }
    ),

  askTribunal: (question: string, documentIds?: string[], topK = 6) =>
    request<import("./types").TribunalResult>("/tribunal/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question,
        document_ids: documentIds,
        top_k: topK,
      }),
    }),

  runEvaluations: () =>
    request<import("./types").EvaluationRun>("/evaluations/run", {
      method: "POST",
    }),

  listEvaluationRuns: () =>
    request<{ runs: import("./types").EvaluationRun[] }>("/evaluations/runs"),
};

export { BACKEND_URL };
