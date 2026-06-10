import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import HomePage from "@/app/page";

describe("HomePage", () => {
  it("renders project title and CTAs", () => {
    render(<HomePage />);
    expect(screen.getByText("The Hallucination Tribunal")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Upload Documents" })).toHaveAttribute(
      "href",
      "/corpus"
    );
    expect(screen.getByRole("link", { name: "Ask the Tribunal" })).toHaveAttribute(
      "href",
      "/tribunal"
    );
  });
});
