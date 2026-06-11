import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { SampleGovernancePanel } from "@/components/corpus/SampleGovernancePanel";

const mockImportSampleDocuments = vi.fn();

vi.mock("@/lib/api/client", () => ({
  api: {
    importSampleDocuments: (...args: unknown[]) => mockImportSampleDocuments(...args),
  },
}));

const sampleLibrary = {
  categories: ["NIST & Federal Standards"],
  samples: [
    {
      sample_id: "nist-ai-rmf",
      title: "NIST AI Risk Management Framework",
      category: "NIST & Federal Standards",
      source: "NIST",
      url: "https://example.com/nist",
      description: "Risk management guidance",
      good_for: "Governance structure",
      filename: "sample-nist-ai-rmf.md",
      already_imported: false,
    },
  ],
};

describe("SampleGovernancePanel", () => {
  it("renders sample picker and imports selected document", async () => {
    mockImportSampleDocuments.mockResolvedValue({
      imported: [
        {
          sample_id: "nist-ai-rmf",
          document_id: "doc-1",
          filename: "sample-nist-ai-rmf.md",
          status: "indexed",
          chunk_count: 2,
        },
      ],
      skipped: [],
      errors: [],
    });

    render(
      <SampleGovernancePanel
        samples={sampleLibrary.samples}
        categories={sampleLibrary.categories}
      />
    );
    expect(await screen.findByLabelText("Governance document")).toBeInTheDocument();
    expect(screen.getByText("Risk management guidance")).toBeInTheDocument();
    await userEvent.click(screen.getByRole("button", { name: "Add Selected Document" }));
    expect(mockImportSampleDocuments).toHaveBeenCalledWith(["nist-ai-rmf"]);
    expect(await screen.findByRole("status")).toHaveTextContent("1 added");
  });
});
