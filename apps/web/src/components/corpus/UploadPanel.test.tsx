import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { UploadPanel } from "@/components/corpus/UploadPanel";

vi.mock("@/lib/api/client", () => ({
  api: {
    uploadDocument: vi.fn().mockResolvedValue({
      document_id: "1",
      filename: "policy.md",
      status: "indexed",
      chunk_count: 3,
    }),
  },
}));

describe("UploadPanel", () => {
  it("renders upload button with accessible label", () => {
    render(<UploadPanel />);
    expect(screen.getByRole("button", { name: "Choose File" })).toBeInTheDocument();
  });

  it("shows status after successful upload", async () => {
    render(<UploadPanel />);
    const input = screen.getByLabelText("Choose document file");
    const file = new File(["# Policy"], "policy.md", { type: "text/markdown" });
    await userEvent.upload(input, file);
    expect(await screen.findByRole("status")).toHaveTextContent("Indexed policy.md");
  });
});
