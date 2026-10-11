// Django supplies the manifest URL so changes to the shared module invalidate caches.
const { mountCosmicScene } = await import(
  document.querySelector("script[data-cosmic-module]").dataset.cosmicModule
);

function mountAtmosphere() {
  const host = document.createElement("div");
  host.className = "api-docs-atmosphere";
  host.setAttribute("aria-hidden", "true");
  document.body.prepend(host);
  const scene = mountCosmicScene(host, { stars: true });
  const surfaces = [
    ...document.querySelectorAll(".api-docs-notes, .api-docs-account-guide"),
  ];
  surfaces.forEach((element) => element.classList.add("iz2-spotlight"));
  const controller = new AbortController();
  const options = { passive: true, signal: controller.signal };
  let active = false;
  let frame = null;
  let pointer = null;
  const reset = () => {
    pointer = null;
    if (frame !== null) cancelAnimationFrame(frame);
    frame = null;
    surfaces.forEach((element) => {
      element.dataset.spotlightNear = "false";
    });
  };
  const update = () => {
    active =
      document.documentElement.dataset.apiMotion === "on" && !document.hidden;
    scene.setActive(active);
    surfaces.forEach((element) => {
      element.dataset.spotlightMotion = active ? "on" : "off";
    });
    if (!active) reset();
  };
  const observer = new MutationObserver(update);
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-api-motion"],
  });
  document.addEventListener("visibilitychange", update, options);
  window.addEventListener(
    "pointermove",
    (event) => {
      if (!active || event.pointerType === "touch") return;
      pointer = { x: event.clientX, y: event.clientY };
      if (frame !== null) return;
      frame = requestAnimationFrame(() => {
        frame = null;
        if (!pointer) return;
        for (const element of surfaces) {
          const box = element.getBoundingClientRect();
          const x = Math.min(Math.max(pointer.x - box.left, 0), box.width);
          const y = Math.min(Math.max(pointer.y - box.top, 0), box.height);
          const distance = Math.hypot(
            pointer.x - box.left - x,
            pointer.y - box.top - y,
          );
          const strength = Math.max(0, 1 - distance / 48);
          element.dataset.spotlightNear = String(strength > 0);
          // Retain the last position during fade-out, just like the workspace.
          if (strength > 0) {
            element.style.setProperty("--spotlight-x", `${x}px`);
            element.style.setProperty("--spotlight-y", `${y}px`);
            element.style.setProperty("--spotlight-strength", String(strength));
          }
        }
      });
    },
    options,
  );
  window.addEventListener(
    "pointerout",
    (event) => {
      if (event.relatedTarget === null) reset();
    },
    options,
  );
  window.addEventListener("blur", reset, options);
  window.addEventListener("scroll", reset, { ...options, capture: true });
  update();
  return () => {
    controller.abort();
    observer.disconnect();
    reset();
    scene.destroy();
    host.remove();
  };
}

let dispose = mountAtmosphere();
window.addEventListener("pagehide", () => {
  dispose();
});
window.addEventListener("pageshow", (event) => {
  if (event.persisted) dispose = mountAtmosphere();
});
