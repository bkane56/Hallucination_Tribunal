import path from "path";
import { test, expect } from "@playwright/test";

const mockTribunalResult = {
  question: "What does the policy say about external LLM APIs?",
  witness_answer: {
    answer_text: "External LLM APIs require written approval from the security team.",
  },
  prosecutor_objections: [
    {
      objection_id: "obj-1",
      claim_id: "claim-1",
      objection_type: "unsupported",
      explanation: "Needs stronger citation.",
    },
  ],
  judge_verdict: [
    {
      claim_id: "claim-1",
      verdict: "SUSTAINED",
      confidence: 0.82,
      explanation: "Supported by policy text.",
      supporting_sources: ["sample-policy.md"],
    },
  ],
  claims: [
    {
      claim_id: "claim-1",
      claim_text: "External LLM APIs require written approval.",
    },
  ],
  retrieved_sources: [
    {
      chunk_id: "chunk-1",
      filename: "sample-policy.md",
      text: "External LLM APIs require written approval from the security team.",
    },
  ],
  final_answer: "External LLM APIs require written approval from the security team.",
  overall_verdict: "SUSTAINED",
  reliability_score: 0.82,
};

test("upload document on corpus page", async ({ page }) => {
  await page.route("**/documents", async (route) => {
    if (route.request().method() === "GET") {
      await route.fulfill({ json: { documents: [] } });
      return;
    }
    await route.continue();
  });

  await page.route("**/documents/upload", async (route) => {
    await route.fulfill({
      json: {
        document_id: "doc-1",
        filename: "sample-policy.md",
        status: "indexed",
        chunk_count: 2,
      },
    });
  });

  await page.goto("/corpus");
  await page.getByRole("button", { name: "Choose File" }).click();
  await page
    .getByLabel("Choose document file")
    .setInputFiles(path.join(__dirname, "fixtures/sample-policy.md"));

  await expect(page.getByRole("status")).toContainText("Indexed sample-policy.md");
});

test("ask tribunal and review claim docket", async ({ page }) => {
  await page.route("**/tribunal/ask", async (route) => {
    await route.fulfill({ json: mockTribunalResult });
  });

  await page.goto("/tribunal");
  await page
    .getByLabel("Question for the tribunal")
    .fill("What does the policy say about external LLM APIs?");
  await page.getByRole("button", { name: "Run Tribunal" }).click();

  await expect(page.getByText("Tribunal Verdict")).toBeVisible();
  await expect(page.getByText("SUSTAINED").first()).toBeVisible();
  await expect(page.getByRole("heading", { name: "Claim Docket" })).toBeVisible();
  await expect(page.getByText("External LLM APIs require written approval.")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Final Ruling" })).toBeVisible();
});
