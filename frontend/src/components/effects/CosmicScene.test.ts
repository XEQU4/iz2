import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { mountCosmicScene } from "../../../../static/js/cosmic-scene.js";

describe("shared cosmic event lifecycle", () => {
  let host: HTMLDivElement;
  const animations: Array<{
    pause: ReturnType<typeof vi.fn>;
    play: ReturnType<typeof vi.fn>;
    cancel: ReturnType<typeof vi.fn>;
  }> = [];
  beforeEach(() => {
    vi.useFakeTimers({ toFake: ["setTimeout", "clearTimeout", "performance"] });
    vi.spyOn(Math, "random").mockReturnValue(0.5);
    host = document.createElement("div");
    document.body.append(host);
    animations.length = 0;
    vi.stubGlobal("matchMedia", () => ({ matches: false }));
    Object.defineProperty(Element.prototype, "animate", {
      configurable: true,
      value: vi.fn(() => {
        const animation = { pause: vi.fn(), play: vi.fn(), cancel: vi.fn() };
        animations.push(animation);
        return animation as unknown as Animation;
      }),
    });
  });
  afterEach(() => {
    Reflect.deleteProperty(Element.prototype, "animate");
    Reflect.deleteProperty(document, "elementFromPoint");
    host.remove();
    vi.useRealTimers();
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it("leaves a static moon and star field without scheduling disabled motion", () => {
    const scene = mountCosmicScene(host, { stars: true });
    expect(host.querySelector(".iz2-moon")).not.toBeNull();
    expect(host.querySelectorAll(".iz2-cosmos__star")).toHaveLength(150);
    expect(vi.getTimerCount()).toBe(0);
    scene.destroy();
    expect(host.children).toHaveLength(0);
  });

  it("retains remaining event time through suspension and releases all owned work", () => {
    const scene = mountCosmicScene(host);
    scene.setActive(true);
    expect(vi.getTimerCount()).toBe(2);
    vi.advanceTimersByTime(4000);
    scene.setActive(false);
    expect(vi.getTimerCount()).toBe(0);
    vi.advanceTimersByTime(60000);
    expect(animations).toHaveLength(0);
    scene.setActive(true);
    vi.advanceTimersByTime(9999);
    expect(animations).toHaveLength(0);
    vi.advanceTimersByTime(1);
    expect(host.querySelectorAll(".iz2-cosmos__meteor")).toHaveLength(1);
    scene.setActive(false);
    expect(animations[0].pause).toHaveBeenCalledOnce();
    scene.setActive(true);
    expect(animations[0].play).toHaveBeenCalledOnce();
    vi.advanceTimersByTime(22000);
    expect(host.querySelectorAll(".iz2-cosmos__asteroid")).toHaveLength(1);
    scene.destroy();
    expect(vi.getTimerCount()).toBe(0);
    expect(
      animations.every((animation) => animation.cancel.mock.calls.length === 1),
    ).toBe(true);
    expect(host.children).toHaveLength(0);
  });

  it("skips an occurrence when opaque panels occupy every candidate path", () => {
    const panel = document.createElement("div");
    panel.style.backgroundColor = "rgb(25, 27, 30)";
    host.append(panel);
    Object.defineProperty(document, "elementFromPoint", {
      configurable: true,
      value: () => panel,
    });
    const scene = mountCosmicScene(host);
    scene.setActive(true);
    vi.advanceTimersByTime(40000);
    expect(animations).toHaveLength(0);
    expect(vi.getTimerCount()).toBe(2);
    scene.destroy();
    expect(vi.getTimerCount()).toBe(0);
  });
});
