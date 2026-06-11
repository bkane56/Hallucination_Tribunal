import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { CorpusManager } from "@/components/corpus/CorpusManager";

const mockLoadCorpus = vi.fn();
const mockDelete = vi.fn();
const mockRebuild = vi.fn();

vi.mock("@/lib/api/client", () => ({
  api: {
    loadCorpusOverview: (...args: unknown[]) => mockLoadCorpus(...args),
    deleteDocument: (...args: unknown[]) => mockDelete(...args),
    rebuildIndex: (...args: unknown[]) => mockRebuild(...args),
    uploadDocument: vi.fn(),
    importSampleDocuments: vi.fn().mockResolvedValue({ imported: [], skipped: [], errors: [] }),
  },
}));

describe("CorpusManager", () => {
  it("loads and displays documents", async () => {
    mockLoadCorpus.mockResolvedValue({
      documents: [
        {
          document_id: "d1",
          filename: "policy.md",
          file_type: "md",
          chunk_count: 3,
          status: "indexed",
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        },
      ],
      samples: [],
      categories: [],
    });

    render(<CorpusManager />);
    expect(await screen.findByText("policy.md")).toBeInTheDocument();
    expect(screen.getByText("3")).toBeInTheDocument();
  });

  it("deletes a document", async () => {
    mockLoadCorpus.mockResolvedValue({
      documents: [
        {
          document_id: "d1",
          filename: "policy.md",
          file_type: "md",
          chunk_count: 3,
          status: "indexed",
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        },
      ],
      samples: [],
      categories: [],
    });
    mockDelete.mockResolvedValue({ status: "deleted", document_id: "d1" });
    mockLoadCorpus
      .mockResolvedValueOnce({
        documents: [
          {
            document_id: "d1",
            filename: "policy.md",
            file_type: "md",
            chunk_count: 3,
            status: "indexed",
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          },
        ],
        samples: [],
        categories: [],
      })
      .mockResolvedValueOnce({ documents: [], samples: [], categories: [] });

    render(<CorpusManager />);
    await screen.findByText("policy.md");
    await userEvent.click(screen.getByRole("button", { name: "Delete" }));
    await waitFor(() => expect(mockDelete).toHaveBeenCalledWith("d1"));
  });
});
