import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { EvaluationDashboard } from "@/components/evaluation/EvaluationDashboard";

vi.mock("@/lib/api/client", () => {
  const mockRun = {
    run_id: "run-1",
    started_at: new Date().toISOString(),
    completed_at: new Date().toISOString(),
    aggregate_metrics: {
      pass_rate: 0.8,
      retrieval_hit_rate: 0.9,
      avg_citation_accuracy: 0.7,
      total_unsupported_claims: 1,
    },
    case_results: [
      {
        case_id: "c1",
        question: "Are external APIs allowed?",
        retrieval_hit: true,
        citation_accuracy: 0.8,
        unsupported_claim_count: 0,
        contradicted_claim_count: 0,
        reliability_score: 0.9,
        expected_verdict_behavior: "grounded",
        passed: true,
      },
    ],
  };

  return {
    api: {
      runEvaluations: vi.fn().mockResolvedValue(mockRun),
      listEvaluationRuns: vi.fn().mockResolvedValue({ runs: [mockRun] }),
      getEvaluationRun: vi.fn().mockResolvedValue(mockRun),
    },
  };
});

describe("EvaluationDashboard", () => {
  it("runs evaluations and shows metrics", async () => {
    render(<EvaluationDashboard />);
    await userEvent.click(screen.getByRole("button", { name: "Run All Evaluations" }));
    expect(await screen.findByText("Pass Rate")).toBeInTheDocument();
    expect(screen.getByText("80%")).toBeInTheDocument();
    expect(screen.getByText("Are external APIs allowed?")).toBeInTheDocument();
  });

  it("loads run history on mount", async () => {
    render(<EvaluationDashboard />);
    await waitFor(() => {
      expect(screen.getByText("Run History")).toBeInTheDocument();
    });
  });
});
