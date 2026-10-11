// React Bits Glitch Text clip technique, adapted to a quiet monochrome hover echo.
// Copyright (c) 2026 David Haz. MIT + Commons Clause; see licenses/react-bits.txt.
import { useDecorationActive } from "./useDecorationActive";
import "./GlitchText.css";

interface GlitchTextProps {
  text: string;
  className?: string;
  enabled?: boolean;
}

export function GlitchText({
  text,
  className = "",
  enabled = true,
}: GlitchTextProps) {
  const { ref, active } = useDecorationActive<HTMLSpanElement>(enabled);
  return (
    <span ref={ref} className={`iz2-glitch ${className}`} data-active={active}>
      {text}
      <span
        className="iz2-glitch__duplicate iz2-glitch__duplicate--blue"
        data-text={text}
        aria-hidden="true"
      />
      <span
        className="iz2-glitch__duplicate iz2-glitch__duplicate--cyan"
        data-text={text}
        aria-hidden="true"
      />
    </span>
  );
}
