import {
  useCallback,
  useEffect,
  useRef,
  useState,
  type FocusEvent,
  type HTMLAttributes,
  type PointerEvent,
} from "react";
import { useDecorationActive } from "../motion/useDecorationActive";
import { proximityToRect, usePointerProximity } from "./usePointerProximity";
import { cx } from "../../lib/utils";
import "./SpotlightSurface.css";

/** Decorative interaction only: keep the element's original link/button semantics. */
export function useSpotlight<T extends HTMLElement = HTMLDivElement>({
  disabled = false,
}: { disabled?: boolean } = {}) {
  const { ref, active: followsPointer } = useDecorationActive<T>(!disabled);
  const [hovered, setHovered] = useState(false);
  const [focused, setFocused] = useState(false);
  const frame = useRef<number | null>(null);
  const pending = useRef<{
    element: T;
    x: number;
    y: number;
    strength: number;
  } | null>(null);

  const cancel = useCallback(() => {
    if (frame.current !== null) cancelAnimationFrame(frame.current);
    frame.current = null;
    pending.current = null;
  }, []);

  const leave = useCallback(() => {
    setHovered(false);
    cancel();
    if (ref.current) ref.current.dataset.spotlightNear = "false";
  }, [cancel, ref]);

  useEffect(() => {
    if (!followsPointer) leave();
    return cancel;
  }, [cancel, followsPointer, leave]);

  const moveAt = useCallback(
    (element: T, clientX: number, clientY: number) => {
      if (!followsPointer) return;
      const bounds = element.getBoundingClientRect();
      const { x, y, strength } = proximityToRect(bounds, clientX, clientY);
      if (!strength) {
        leave();
        return;
      }
      pending.current = {
        element,
        x,
        y,
        strength,
      };
      if (frame.current !== null) return;
      frame.current = requestAnimationFrame(() => {
        frame.current = null;
        const next = pending.current;
        pending.current = null;
        if (!next?.element.isConnected || document.hidden) return;
        next.element.dataset.spotlightNear = "true";
        next.element.style.setProperty("--spotlight-x", `${next.x}px`);
        next.element.style.setProperty("--spotlight-y", `${next.y}px`);
        next.element.style.setProperty(
          "--spotlight-strength",
          String(next.strength),
        );
      });
    },
    [followsPointer, leave],
  );
  usePointerProximity(ref, followsPointer, moveAt, leave);
  const move = (event: PointerEvent<T>) => {
    if (event.pointerType !== "touch")
      moveAt(event.currentTarget, event.clientX, event.clientY);
  };

  const blur = (event: FocusEvent<T>) => {
    if (
      !event.relatedTarget ||
      !(event.relatedTarget instanceof Node) ||
      !event.currentTarget.contains(event.relatedTarget)
    ) {
      setFocused(false);
    }
  };

  return {
    active: hovered || focused,
    surfaceProps: {
      ref,
      className: "iz2-spotlight",
      "data-spotlight-motion": followsPointer ? "on" : "off",
      onPointerEnter: (event: PointerEvent<T>) => {
        if (event.pointerType !== "touch") setHovered(true);
      },
      onPointerMove: move,
      onPointerLeave: leave,
      onPointerCancel: leave,
      onFocusCapture: () => setFocused(true),
      onBlurCapture: blur,
    } as const,
  };
}

export interface SpotlightSurfaceProps extends HTMLAttributes<HTMLDivElement> {
  disabled?: boolean;
}

/** Wrap arbitrary saved content; this surface adds no tab stop or click action. */
export function SpotlightSurface({
  children,
  className,
  disabled,
  onPointerEnter,
  onPointerMove,
  onPointerLeave,
  onPointerCancel,
  onFocusCapture,
  onBlurCapture,
  ...props
}: SpotlightSurfaceProps) {
  const { surfaceProps } = useSpotlight<HTMLDivElement>({ disabled });
  return (
    <div
      {...props}
      {...surfaceProps}
      className={cx(surfaceProps.className, className)}
      onPointerEnter={(event) => {
        onPointerEnter?.(event);
        if (!event.defaultPrevented) surfaceProps.onPointerEnter(event);
      }}
      onPointerMove={(event) => {
        onPointerMove?.(event);
        if (!event.defaultPrevented) surfaceProps.onPointerMove(event);
      }}
      onPointerLeave={(event) => {
        onPointerLeave?.(event);
        surfaceProps.onPointerLeave();
      }}
      onPointerCancel={(event) => {
        onPointerCancel?.(event);
        surfaceProps.onPointerCancel();
      }}
      onFocusCapture={(event) => {
        onFocusCapture?.(event);
        surfaceProps.onFocusCapture();
      }}
      onBlurCapture={(event) => {
        onBlurCapture?.(event);
        surfaceProps.onBlurCapture(event);
      }}
    >
      {children}
    </div>
  );
}
