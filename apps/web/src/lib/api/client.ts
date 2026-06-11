import type {
  Document,
  EvaluationRun,
  SampleDocument,
  SampleDocumentImportResult,
  TribunalResult,
} from "@/lib/types";

function getApiBaseUrl(): string {
  const explicit = process.env.NEXT_PUBLIC_BACKEND_URL?.trim();
  if (explicit) {
    return explicit.replace(/\/$/, "");
  }

  const routePrefix = process.env.NEXT_PUBLIC_API_ROUTE_PREFIX?.trim();
  if (routePrefix) {
    return routePrefix.replace(/\/$/, "");
  }

  return "http://localhost:8000";
}

const BACKEND_URL = getApiBaseUrl();

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
    request<{ documents: Document[] }>("/documents"),

  loadCorpusOverview: async () => {
    const response = await fetch(`${BACKEND_URL}/corpus/overview`);
    if (response.ok) {
      return response.json() as Promise<{
        documents: Document[];
        samples: SampleDocument[];
        categories: string[];
      }>;
    }
    // Backward-compatible fallback when API is not yet redeployed with /corpus/overview
    if (response.status === 404) {
      const [documents, samples] = await Promise.all([
        request<{ documents: Document[] }>("/documents"),
        request<{ samples: SampleDocument[]; categories: string[] }>("/documents/samples"),
      ]);
      return {
        documents: documents.documents,
        samples: samples.samples,
        categories: samples.categories,
      };
    }
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(error.detail || "Request failed");
  },

  uploadDocument: async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return request<{ document_id: string; filename: string; status: string; chunk_count: number }>(
      "/documents/upload",
      { method: "POST", body: formData }
    );
  },

  listSampleDocuments: () =>
    request<{ samples: SampleDocument[]; categories: string[] }>(
      "/documents/samples"
    ),

  importSampleDocuments: (sampleIds: string[]) =>
    request<{
      imported: SampleDocumentImportResult[];
      skipped: SampleDocumentImportResult[];
      errors: SampleDocumentImportResult[];
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
    request<TribunalResult>("/tribunal/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question,
        document_ids: documentIds,
        top_k: topK,
      }),
    }),

  runEvaluations: () =>
    request<EvaluationRun>("/evaluations/run", {
      method: "POST",
    }),

  listEvaluationRuns: () =>
    request<{ runs: EvaluationRun[] }>("/evaluations/runs"),
};

export { BACKEND_URL };
