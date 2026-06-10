import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { CorpusManager } from "@/components/corpus/CorpusManager";

const mockList = vi.fn();
const mockDelete = vi.fn();
const mockRebuild = vi.fn();

vi.mock("@/lib/api/client", () => ({
  api: {
    listDocuments: (...args: unknown[]) => mockList(...args),
    deleteDocument: (...args: unknown[]) => mockDelete(...args),
    rebuildIndex: (...args: unknown[]) => mockRebuild(...args),
    uploadDocument: vi.fn(),
  },
}));

describe("CorpusManager", () => {
  it("loads and displays documents", async () => {
    mockList.mockResolvedValue({
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
    });

    render(<CorpusManager />);
    expect(await screen.findByText("policy.md")).toBeInTheDocument();
    expect(screen.getByText("3")).toBeInTheDocument();
  });

  it("deletes a document", async () => {
    mockList.mockResolvedValue({
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
    });
    mockDelete.mockResolvedValue({ status: "deleted", document_id: "d1" });
    mockList.mockResolvedValueOnce({
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
    }).mockResolvedValueOnce({ documents: [] });

    render(<CorpusManager />);
    await screen.findByText("policy.md");
    await userEvent.click(screen.getByRole("button", { name: "Delete" }));
    await waitFor(() => expect(mockDelete).toHaveBeenCalledWith("d1"));
  });
});
