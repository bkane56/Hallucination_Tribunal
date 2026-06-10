import { describe, expect, it } from "vitest";
import { formatReliability, verdictColor } from "@/lib/utils";

describe("verdictColor", () => {
  it("returns teal styling for Supported", () => {
    expect(verdictColor("Supported")).toContain("verdict-teal");
  });

  it("returns amber styling for Partially Supported", () => {
    expect(verdictColor("Partially Supported")).toContain("objection-amber");
  });

  it("returns red styling for Unsupported", () => {
    expect(verdictColor("Unsupported")).toContain("overruled-red");
  });

  it("returns default styling for unknown verdict", () => {
    expect(verdictColor("Unknown")).toContain("charcoal");
  });
});

describe("formatReliability", () => {
  it("formats numeric scores as percentages", () => {
    expect(formatReliability(0.78)).toBe("78%");
  });

  it("returns Not Applicable unchanged", () => {
    expect(formatReliability("Not Applicable")).toBe("Not Applicable");
  });

  it("returns string scores unchanged", () => {
    expect(formatReliability("0.75")).toBe("0.75");
  });
});
