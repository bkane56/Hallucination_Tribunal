import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { TribunalPanel } from "@/components/tribunal/TribunalPanel";

vi.mock("@/lib/api/client", () => ({
  api: {
    askTribunal: vi.fn().mockResolvedValue({
      tribunal_result_id: "t1",
      question: "test",
      final_answer: "Final ruling text",
      overall_verdict: "Supported",
      reliability_score: 0.9,
      retrieved_sources: [
        {
          chunk_id: "c1",
          document_id: "d1",
          filename: "policy.md",
          text: "Approval required.",
          similarity_score: 0.9,
        },
      ],
      witness_answer: { answer_text: "Witness text", citations: [] },
      claims: [
        {
          claim_id: "claim-1",
          claim_text: "Approval required.",
          claim_type: "factual",
          cited_sources: [],
          extracted_from_sentence: "Approval required.",
        },
      ],
      prosecutor_objections: [],
      judge_verdict: [
        {
          claim_id: "claim-1",
          verdict: "Supported",
          confidence: 0.9,
          explanation: "Supported",
          supporting_sources: ["policy.md"],
          recommended_revision: null,
        },
      ],
      created_at: new Date().toISOString(),
    }),
  },
}));

describe("TribunalPanel", () => {
  it("runs tribunal and shows final ruling", async () => {
    render(<TribunalPanel />);
    await userEvent.type(
      screen.getByLabelText("Question for the tribunal"),
      "Are external APIs allowed?"
    );
    await userEvent.click(screen.getByRole("button", { name: "Run Tribunal" }));
    expect(await screen.findByText("Final Ruling")).toBeInTheDocument();
    expect(screen.getByText("Final ruling text")).toBeInTheDocument();
    expect(screen.getByText("Claim Docket")).toBeInTheDocument();
  });
});
