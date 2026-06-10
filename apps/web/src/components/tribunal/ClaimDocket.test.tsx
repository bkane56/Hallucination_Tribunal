import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { ClaimDocket } from "@/components/tribunal/ClaimDocket";

const claims = [
  {
    claim_id: "c1",
    claim_text: "Approval is required.",
    claim_type: "factual",
    cited_sources: [],
    extracted_from_sentence: "Approval is required for external APIs.",
  },
];

const verdicts = [
  {
    claim_id: "c1",
    verdict: "Supported" as const,
    confidence: 0.92,
    explanation: "Directly supported by policy.",
    supporting_sources: ["policy.md"],
    recommended_revision: null,
  },
];

describe("ClaimDocket", () => {
  it("renders claim docket table headers", () => {
    render(
      <ClaimDocket claims={claims} verdicts={verdicts} objections={[]} sources={[]} />
    );
    expect(screen.getByText("Claim Docket")).toBeInTheDocument();
    expect(screen.getByText("Claim")).toBeInTheDocument();
    expect(screen.getByText("Verdict")).toBeInTheDocument();
  });

  it("expands row details on click", async () => {
    render(
      <ClaimDocket claims={claims} verdicts={verdicts} objections={[]} sources={[]} />
    );
    await userEvent.click(screen.getByText("Approval is required."));
    expect(screen.getByText(/Original sentence/)).toBeInTheDocument();
  });

  it("shows empty state when no claims", () => {
    render(<ClaimDocket claims={[]} verdicts={[]} objections={[]} sources={[]} />);
    expect(screen.getByText(/No factual claims/)).toBeInTheDocument();
  });
});
