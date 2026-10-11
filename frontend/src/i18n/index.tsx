import {
  useCallback,
  useEffect,
  useSyncExternalStore,
  type ReactNode,
} from "react";
import { commonMessages } from "./common";
import { entityMessages } from "./entities";
import { graphMessages } from "./graph";
import { shellMessages } from "./shell";

export type Language = "en" | "ru";
export type MessageValues = Record<string, string | number>;
export const LANGUAGE_STORAGE_KEY = "iz2-language";
const messages: Record<string, string> = {
  ...commonMessages,
  ...entityMessages,
  ...graphMessages,
  ...shellMessages,
};
const listeners = new Set<() => void>();

function readPreference(): Language {
  try {
    return localStorage.getItem(LANGUAGE_STORAGE_KEY) === "ru" ? "ru" : "en";
  } catch {
    return "en";
  }
}
let language: Language = readPreference();
export function getLanguage(): Language {
  return language;
}
export function setLanguage(next: Language): void {
  if (next !== "en" && next !== "ru") return;
  try {
    localStorage.setItem(LANGUAGE_STORAGE_KEY, next);
  } catch {
    /* The in-memory preference remains usable. */
  }
  if (next === language) return;
  language = next;
  listeners.forEach((notify) => notify());
}
function storageChanged(event: StorageEvent): void {
  if (event.key !== LANGUAGE_STORAGE_KEY && event.key !== null) return;
  const next = readPreference();
  if (next === language) return;
  language = next;
  listeners.forEach((notify) => notify());
}
function subscribe(notify: () => void): () => void {
  if (listeners.size === 0) window.addEventListener("storage", storageChanged);
  listeners.add(notify);
  return () => {
    listeners.delete(notify);
    if (listeners.size === 0)
      window.removeEventListener("storage", storageChanged);
  };
}

/** Translate application messages only. Source values and saved prose remain original. */
export function translate(
  message: string,
  values?: MessageValues,
  selected: Language = language,
): string {
  const pattern =
    selected === "ru" && Object.prototype.hasOwnProperty.call(messages, message)
      ? messages[message]
      : message;
  return pattern.replace(/\{(\w+)\}/g, (placeholder, key: string) =>
    values && Object.prototype.hasOwnProperty.call(values, key)
      ? String(values[key])
      : placeholder,
  );
}
export function useI18n() {
  const selected = useSyncExternalStore(
    subscribe,
    getLanguage,
    () => "en" as Language,
  );
  const t = useCallback(
    (message: string, values?: MessageValues) =>
      translate(message, values, selected),
    [selected],
  );
  return {
    language: selected,
    locale: selected === "ru" ? ("ru-RU" as const) : ("en-US" as const),
    t,
    setLanguage,
  };
}

export function LanguageProvider({ children }: { children: ReactNode }) {
  const { language: selected } = useI18n();
  useEffect(() => {
    document.documentElement.lang = selected;
  }, [selected]);
  return children;
}

export function LanguageSwitch() {
  const { language: selected } = useI18n();
  return (
    <button
      type="button"
      className="language-switch"
      onClick={() => setLanguage(selected === "en" ? "ru" : "en")}
      aria-label={
        selected === "en" ? "Switch to Russian" : "Переключить на английский"
      }
      title="English / Русский"
      data-language={selected}
    >
      <span
        className={`language-flag${selected === "en" ? " active" : ""}`}
        title="English"
        aria-hidden="true"
      >
        <svg viewBox="0 0 60 40" focusable="false">
          <path fill="#334261" d="M0 0h60v40H0z" />
          <path stroke="#f4f3ef" strokeWidth="9" d="m0 0 60 40m0-40L0 40" />
          <path stroke="#b7535a" strokeWidth="3" d="m0 0 60 40m0-40L0 40" />
          <path stroke="#f4f3ef" strokeWidth="13" d="M30 0v40M0 20h60" />
          <path stroke="#b7535a" strokeWidth="7" d="M30 0v40M0 20h60" />
        </svg>
      </span>
      <span
        className={`language-flag${selected === "ru" ? " active" : ""}`}
        title="Русский"
        aria-hidden="true"
      >
        <svg viewBox="0 0 60 40" focusable="false">
          <path fill="#f4f3ef" d="M0 0h60v14H0z" />
          <path fill="#51699c" d="M0 14h60v13H0z" />
          <path fill="#b7535a" d="M0 27h60v13H0z" />
        </svg>
      </span>
    </button>
  );
}
