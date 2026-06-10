import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { AppShell } from "@/components/layout/AppShell";

describe("AppShell", () => {
  it("renders header, privacy banner, and footer", () => {
    render(
      <AppShell>
        <p>Child content</p>
      </AppShell>
    );
    expect(screen.getByText("The Hallucination Tribunal")).toBeInTheDocument();
    expect(screen.getByText(/Privacy note/)).toBeInTheDocument();
    expect(screen.getByText("Child content")).toBeInTheDocument();
  });
});
