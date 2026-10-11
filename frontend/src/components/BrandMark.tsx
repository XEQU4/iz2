import logo from "../assets/branding/iz2-logo.png";

/** Original transparent PNG; the containing link supplies its accessible name. */
export function BrandMark({ compact = false }: { compact?: boolean }) {
  return (
    <img
      className={`brand-artwork${compact ? " brand-artwork--compact" : ""}`}
      src={logo}
      alt=""
      width={1254}
      height={1254}
    />
  );
}
