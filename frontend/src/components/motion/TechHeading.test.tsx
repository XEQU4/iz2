import { act, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { TechHeading } from "./TechHeading";
import { MotionPreferences, useMotionPreferences } from "../MotionPreferences";

beforeEach(() => vi.useFakeTimers());
afterEach(() => {
  vi.useRealTimers();
  vi.restoreAllMocks();
  localStorage.clear();
});

describe("TechHeading reveal completion", () => {
  it("finishes even when hovering the final glyph cancels its CSS animation", () => {
    const { container } = render(<TechHeading as="h1" text="HELLO" />);
    const heading = screen.getByRole("heading", { name: "HELLO" });
    const glyphs = container.querySelectorAll(".tech-heading__glyph");
    fireEvent.pointerEnter(glyphs[glyphs.length - 1]);
    expect(glyphs[glyphs.length - 1]).toHaveAttribute("data-selected", "true");
    expect(heading).toHaveAttribute("data-revealed", "false");
    act(() => vi.advanceTimersByTime(800));
    expect(heading).toHaveAttribute("data-revealed", "true");
  });

  it("cancels pending completion when the document becomes hidden", () => {
    let hidden = false;
    vi.spyOn(document, "hidden", "get").mockImplementation(() => hidden);
    render(<TechHeading as="h1" text="HELLO" />);
    const heading = screen.getByRole("heading", { name: "HELLO" });
    hidden = true;
    fireEvent(document, new Event("visibilitychange"));
    act(() => vi.advanceTimersByTime(2000));
    expect(heading).toHaveAttribute("data-revealed", "false");
    hidden = false;
    fireEvent(document, new Event("visibilitychange"));
    act(() => vi.advanceTimersByTime(800));
    expect(heading).toHaveAttribute("data-revealed", "true");
  });

  it("does not retain a completion timer after unmount", () => {
    const { unmount } = render(<TechHeading as="h1" text="HELLO" />);
    expect(vi.getTimerCount()).toBeGreaterThan(0);
    unmount();
    expect(vi.getTimerCount()).toBe(0);
  });

  it("retains the previous outline for its fade while moving between glyphs", () => {
    const { container } = render(<TechHeading as="h1" text="AB" />);
    const glyphs = container.querySelectorAll(".tech-heading__glyph");
    const outline = glyphs[0].querySelector(".tech-heading__outline");
    fireEvent.pointerEnter(glyphs[0]);
    fireEvent.pointerLeave(glyphs[0]);
    fireEvent.pointerEnter(glyphs[1]);
    expect(glyphs[0]).toHaveAttribute("data-selected", "false");
    expect(glyphs[1]).toHaveAttribute("data-selected", "true");
    expect(glyphs[0].querySelector(".tech-heading__outline")).toBe(outline);
    expect(container.querySelectorAll(".tech-heading__measure")).toHaveLength(
      1,
    );
    fireEvent.pointerLeave(screen.getByRole("heading"));
    expect(container.querySelectorAll('[data-selected="true"]')).toHaveLength(
      0,
    );
    expect(container.querySelectorAll(".tech-heading__measure")).toHaveLength(
      0,
    );
    expect(glyphs[0].querySelector(".tech-heading__outline")).toBe(outline);
  });

  it("clears a hovered glyph when motion is disabled and never resumes stale selection", () => {
    function Toggle() {
      const { toggle } = useMotionPreferences();
      return <button onClick={toggle}>Motion</button>;
    }
    const { container } = render(
      <MotionPreferences>
        <TechHeading as="h1" text="AB" />
        <Toggle />
      </MotionPreferences>,
    );
    const glyph = container.querySelector(".tech-heading__glyph")!;
    fireEvent.pointerEnter(glyph);
    expect(glyph).toHaveAttribute("data-selected", "true");
    fireEvent.click(screen.getByRole("button", { name: "Motion" }));
    expect(screen.getByRole("heading")).toHaveAttribute(
      "data-enabled",
      "false",
    );
    expect(glyph).toHaveAttribute("data-selected", "false");
    expect(vi.getTimerCount()).toBe(0);
    fireEvent.click(screen.getByRole("button", { name: "Motion" }));
    expect(glyph).toHaveAttribute("data-selected", "false");
    expect(screen.getByRole("heading")).toHaveAttribute(
      "data-revealed",
      "true",
    );
  });
});
