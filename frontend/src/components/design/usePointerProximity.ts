import { useEffect, type RefObject } from "react";

export const SURFACE_PROXIMITY = 48;

/** Extend an existing surface effect into its gutter without adding a hit target. */
export function usePointerProximity<T extends HTMLElement>(
  ref: RefObject<T | null>,
  active: boolean,
  move: (target: T, clientX: number, clientY: number) => void,
  reset: () => void,
) {
  useEffect(() => {
    if (!active) return;
    const pointer = (event: PointerEvent) => {
      if (event.pointerType === "touch") return;
      const target = ref.current;
      if (target) move(target, event.clientX, event.clientY);
    };
    const leaveWindow = (event: PointerEvent) => {
      if (event.relatedTarget === null) reset();
    };
    window.addEventListener("pointermove", pointer, { passive: true });
    window.addEventListener("pointerout", leaveWindow);
    window.addEventListener("blur", reset);
    window.addEventListener("scroll", reset, true);
    return () => {
      window.removeEventListener("pointermove", pointer);
      window.removeEventListener("pointerout", leaveWindow);
      window.removeEventListener("blur", reset);
      window.removeEventListener("scroll", reset, true);
      reset();
    };
  }, [active, move, ref, reset]);
}

export function proximityToRect(
  box: DOMRect,
  clientX: number,
  clientY: number,
) {
  const x = Math.min(Math.max(clientX - box.left, 0), box.width);
  const y = Math.min(Math.max(clientY - box.top, 0), box.height);
  const distance = Math.hypot(clientX - box.left - x, clientY - box.top - y);
  return { x, y, strength: Math.max(0, 1 - distance / SURFACE_PROXIMITY) };
}
