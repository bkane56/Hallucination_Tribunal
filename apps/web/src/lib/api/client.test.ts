import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { api, BACKEND_URL } from "@/lib/api/client";

describe("api client", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("exposes backend url", () => {
    expect(BACKEND_URL).toContain("localhost");
  });

  it("calls health endpoint", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => ({ status: "ok", version: "0.1.0" }),
    } as Response);

    const result = await api.health();
    expect(result.status).toBe("ok");
    expect(fetch).toHaveBeenCalledWith(`${BACKEND_URL}/health`, undefined);
  });

  it("lists documents", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => ({ documents: [] }),
    } as Response);

    const result = await api.listDocuments();
    expect(result.documents).toEqual([]);
  });

  it("uploads a document with form data", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => ({
        document_id: "doc-1",
        filename: "policy.md",
        status: "indexed",
        chunk_count: 4,
      }),
    } as Response);

    const file = new File(["# Policy"], "policy.md", { type: "text/markdown" });
    const result = await api.uploadDocument(file);

    expect(result.chunk_count).toBe(4);
    expect(fetch).toHaveBeenCalledWith(
      `${BACKEND_URL}/documents/upload`,
      expect.objectContaining({ method: "POST", body: expect.any(FormData) })
    );
  });

  it("deletes a document", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => ({ status: "deleted", document_id: "doc-1" }),
    } as Response);

    const result = await api.deleteDocument("doc-1");
    expect(result.status).toBe("deleted");
    expect(fetch).toHaveBeenCalledWith(
      `${BACKEND_URL}/documents/doc-1`,
      expect.objectContaining({ method: "DELETE" })
    );
  });

  it("rebuilds the index", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => ({ rebuilt_count: 2, total_documents: 2 }),
    } as Response);

    const result = await api.rebuildIndex();
    expect(result.rebuilt_count).toBe(2);
  });

  it("runs evaluations", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => ({ run_id: "run-1", pass_rate: 0.8 }),
    } as Response);

    const result = await api.runEvaluations();
    expect(result.run_id).toBe("run-1");
  });

  it("lists evaluation runs", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => ({ runs: [] }),
    } as Response);

    const result = await api.listEvaluationRuns();
    expect(result.runs).toEqual([]);
  });

  it("throws on failed request with detail", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: false,
      statusText: "Bad Request",
      json: async () => ({ detail: "Upload failed" }),
    } as Response);

    await expect(api.listDocuments()).rejects.toThrow("Upload failed");
  });

  it("throws on failed request without json body", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: false,
      statusText: "Server Error",
      json: async () => {
        throw new Error("not json");
      },
    } as Response);

    await expect(api.listDocuments()).rejects.toThrow("Server Error");
  });

  it("throws generic message when detail is missing", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: false,
      statusText: "Bad Gateway",
      json: async () => ({}),
    } as Response);

    await expect(api.listDocuments()).rejects.toThrow("Request failed");
  });

  it("loads corpus overview", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => ({
        documents: [],
        samples: [{ sample_id: "nist-ai-rmf", title: "NIST AI RMF" }],
        categories: ["NIST & Federal Standards"],
      }),
    } as Response);

    const result = await api.loadCorpusOverview();
    expect(result.samples).toHaveLength(1);
    expect(fetch).toHaveBeenCalledWith(`${BACKEND_URL}/corpus/overview`, undefined);
  });

  it("lists sample governance documents", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => ({
        samples: [{ sample_id: "nist-ai-rmf", title: "NIST AI RMF" }],
        categories: ["NIST & Federal Standards"],
      }),
    } as Response);

    const result = await api.listSampleDocuments();
    expect(result.samples).toHaveLength(1);
    expect(fetch).toHaveBeenCalledWith(`${BACKEND_URL}/documents/samples`, undefined);
  });

  it("imports sample governance documents", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => ({ imported: [], skipped: [], errors: [] }),
    } as Response);

    await api.importSampleDocuments(["nist-ai-rmf", "nist-airc"]);
    expect(fetch).toHaveBeenCalledWith(
      `${BACKEND_URL}/documents/samples/import`,
      expect.objectContaining({
        method: "POST",
        headers: { "Content-Type": "application/json" },
      })
    );
  });

  it("asks tribunal with JSON body", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => ({ question: "q", final_answer: "a" }),
    } as Response);

    await api.askTribunal("What is the policy?", ["doc-1"], 4);
    expect(fetch).toHaveBeenCalledWith(
      `${BACKEND_URL}/tribunal/ask`,
      expect.objectContaining({
        method: "POST",
        headers: { "Content-Type": "application/json" },
      })
    );
  });
});
