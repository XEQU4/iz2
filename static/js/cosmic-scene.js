// Shared, framework-independent decoration for the workspace and Django docs.
let sceneId = 0;

function randomSequence() {
  let seed = 160640020;
  return () => {
    seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
    return seed / 4294967296;
  };
}

function moon(id) {
  const random = randomSequence();
  const craters = Array.from({ length: 35 }, (_, index) => {
    const angle = random() * Math.PI * 2;
    const radius = Math.sqrt(random()) * 43;
    const x = 60 + Math.cos(angle) * radius;
    const y = 60 + Math.sin(angle) * radius;
    const size = index < 7 ? 2.2 + random() * 3.6 : 0.5 + random() * 1.2;
    return `<circle cx="${x}" cy="${y}" r="${size}" fill="url(#${id}-crater)"/>`;
  }).join("");
  return `<svg class="iz2-moon" viewBox="0 0 120 120" focusable="false">
    <defs>
      <radialGradient id="${id}-light" cx="77%" cy="28%" r="87%">
        <stop stop-color="#e2e3e1"/><stop offset=".55" stop-color="#929695"/><stop offset="1" stop-color="#373b3e"/>
      </radialGradient>
      <radialGradient id="${id}-halo"><stop offset=".62" stop-color="#dfe4e8" stop-opacity=".07"/><stop offset="1" stop-color="#dfe4e8" stop-opacity="0"/></radialGradient>
      <radialGradient id="${id}-shadow" cx="0%" cy="45%" r="97%">
        <stop offset=".31" stop-color="#080b0f" stop-opacity=".96"/><stop offset=".53" stop-color="#101318" stop-opacity=".88"/>
        <stop offset=".64" stop-color="#171b20" stop-opacity=".5"/><stop offset=".76" stop-color="#171b20" stop-opacity=".08"/><stop offset="1" stop-color="#171b20" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="${id}-crater" cx="34%" cy="30%" r="70%">
        <stop stop-color="#33383b" stop-opacity=".65"/><stop offset=".63" stop-color="#565c5d" stop-opacity=".38"/>
        <stop offset=".82" stop-color="#eff0eb" stop-opacity=".42"/><stop offset="1" stop-color="#b7bbba" stop-opacity="0"/>
      </radialGradient>
      <clipPath id="${id}-disc"><circle cx="60" cy="60" r="48"/></clipPath>
      <filter id="${id}-grain"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" seed="7"/><feColorMatrix type="saturate" values="0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
    </defs>
    <circle class="iz2-moon__halo" cx="60" cy="60" r="60" fill="url(#${id}-halo)"/>
    <g clip-path="url(#${id}-disc)">
      <circle cx="60" cy="60" r="48" fill="url(#${id}-light)"/>
      <g fill="#424b50" opacity=".36">
        <path d="M40 27c5-10 20-9 25-1s-2 14-8 15-6 12-16 9-12-16-1-23Z"/>
        <path d="M70 32c7-8 19-3 22 5s-5 12-6 18-11 13-17 5 3-13-2-18Z"/>
        <path d="M48 56c12-7 22-3 24 6s-7 11-5 18-10 15-19 7-13-24 0-31Z"/>
        <path d="M28 55c7-4 14 0 15 8s-4 14-11 11-12-13-4-19Z"/>
      </g>
      <circle cx="60" cy="60" r="48" filter="url(#${id}-grain)" opacity=".14"/>
      ${craters}
      <circle class="iz2-moon__shade" cx="60" cy="60" r="49" fill="url(#${id}-shadow)"/>
      <path d="M82 17a48 48 0 0 1 18 70" fill="none" stroke="#f1f3f2" stroke-opacity=".3" stroke-width=".5"/>
    </g>
  </svg>`;
}

export function mountCosmicScene(host, { stars = false } = {}) {
  const scene = document.createElement("div");
  scene.className = "iz2-cosmos";
  scene.dataset.active = "false";
  scene.setAttribute("aria-hidden", "true");
  scene.innerHTML = moon(`iz2-cosmos-${++sceneId}`);
  const random = randomSequence();
  const field = document.createElement("div");
  field.className = "iz2-cosmos__stars";
  // API uses this lightweight field; React retains its existing WebGL stars.
  for (let index = 0; index < (stars ? 150 : 18); index++) {
    const star = document.createElement("i");
    star.className = `iz2-cosmos__star${index % 13 === 0 ? " iz2-cosmos__star--bright" : ""}`;
    const size = index % 13 === 0 ? 2.4 : 0.7 + random() * 1.3;
    star.style.cssText = `left:${random() * 100}%;top:${random() * 100}%;width:${size}px;height:${size}px;--star-alpha:${0.25 + random() * 0.5};--star-period:${6 + random() * 9}s;--star-delay:${-random() * 20}s`;
    field.append(star);
  }
  scene.append(field);
  const constellations = document.createElement("div");
  constellations.className = "iz2-cosmos__constellations";
  constellations.innerHTML = `<svg viewBox="0 0 180 120" class="iz2-constellation iz2-constellation--one"><path d="m8 88 43-48 48 21 23-46 46 40M51 40l13 65 35-44"/><g><circle cx="8" cy="88" r="1.6"/><circle cx="51" cy="40" r="2"/><circle cx="99" cy="61" r="1.5"/><circle cx="122" cy="15" r="1.8"/><circle cx="168" cy="55" r="1.4"/><circle cx="64" cy="105" r="1.3"/></g></svg>
    <svg viewBox="0 0 180 120" class="iz2-constellation iz2-constellation--two"><path d="m15 44 53-23 22 57 61 21M90 78l47-53"/><g><circle cx="15" cy="44" r="1.3"/><circle cx="68" cy="21" r="1.7"/><circle cx="90" cy="78" r="2"/><circle cx="151" cy="99" r="1.4"/><circle cx="137" cy="25" r="1.3"/></g></svg>`;
  scene.append(constellations);
  host.append(scene);
  let active = false;
  let destroyed = false;
  const events = new Set();
  const mobile = () => window.matchMedia("(max-width: 767px)").matches;
  const schedules = [
    {
      type: "meteor",
      remaining: 11000 + Math.random() * 6000,
      timer: null,
      started: 0,
    },
    {
      type: "asteroid",
      remaining: 29000 + Math.random() * 14000,
      timer: null,
      started: 0,
    },
  ];

  function openPath(dx, dy) {
    const styles = new Map();
    const clear = (x, y) => {
      if (x < 8 || y < 8 || x > innerWidth - 8 || y > innerHeight - 8)
        return false;
      let element = document.elementFromPoint?.(x, y);
      if (
        element?.closest(
          "a, button, input, select, textarea, h1, h2, h3, p, label",
        )
      )
        return false;
      while (element && element !== document.body) {
        if (!styles.has(element))
          styles.set(element, getComputedStyle(element));
        const style = styles.get(element);
        const channels = style.backgroundColor.match(/[\d.]+/g) ?? [];
        const alpha =
          channels.length === 4
            ? Number(channels[3])
            : channels.length === 3
              ? 1
              : 0;
        if (alpha > 0.6 || style.backgroundImage !== "none") return false;
        element = element.parentElement;
      }
      return true;
    };
    // Check only when an event starts, not every frame. Prefer the upper sky;
    // if content fills it, use another open area or skip this occurrence.
    for (let attempt = 0; attempt < 48; attempt++) {
      const x = innerWidth * (0.25 + Math.random() * 0.68);
      const y =
        innerHeight * (0.09 + Math.random() * (attempt < 28 ? 0.16 : 0.77));
      if ([0, 0.25, 0.5, 0.75, 1].every((t) => clear(x + dx * t, y + dy * t)))
        return { x, y };
    }
    return null;
  }

  function launch(type) {
    if (!scene.animate) return;
    const meteor = type === "meteor";
    const item = document.createElement("i");
    item.className = `iz2-cosmos__${type}`;
    const fromRight = Math.random() > 0.5;
    const dx =
      (meteor ? -1 : fromRight ? -1 : 1) *
      (mobile() ? 120 : meteor ? 260 + Math.random() * 140 : 160);
    const dy = meteor
      ? (mobile() ? 30 : 55) + Math.random() * 45
      : -15 + Math.random() * 30;
    const path = openPath(dx, dy);
    if (!path) return;
    item.style.top = `${path.y}px`;
    item.style.left = `${path.x}px`;
    const angle = meteor ? (Math.atan2(-dy, -dx) * 180) / Math.PI : -20;
    scene.append(item);
    const transform = (fraction, rotation) =>
      `translate(${dx * fraction}px, ${dy * fraction}px) rotate(${rotation}deg)`;
    const animation = item.animate(
      [
        { transform: transform(0, angle), opacity: 0 },
        {
          transform: transform(0.15, angle),
          opacity: meteor ? 0.65 : 0.48,
          offset: 0.15,
        },
        {
          transform: transform(0.72, meteor ? angle : 50),
          opacity: meteor ? 0.45 : 0.48,
          offset: 0.72,
        },
        { transform: transform(1, meteor ? angle : 85), opacity: 0 },
      ],
      {
        duration: meteor
          ? 1800 + Math.random() * 900
          : 22000 + Math.random() * 8000,
        easing: "linear",
      },
    );
    const event = { item, animation };
    events.add(event);
    animation.onfinish = () => {
      events.delete(event);
      item.remove();
    };
  }
  function schedule(job) {
    job.started = performance.now();
    job.timer = window.setTimeout(() => {
      job.timer = null;
      if (!active || destroyed) return;
      launch(job.type);
      job.remaining =
        job.type === "meteor"
          ? 10000 + Math.random() * 10000
          : (mobile() ? 65000 : 42000) + Math.random() * 20000;
      schedule(job);
    }, job.remaining);
  }
  return {
    setActive(value) {
      if (destroyed || active === value) return;
      active = value;
      scene.dataset.active = String(active);
      for (const event of events)
        active ? event.animation.play() : event.animation.pause();
      for (const job of schedules) {
        if (active) schedule(job);
        else if (job.timer !== null) {
          clearTimeout(job.timer);
          job.timer = null;
          job.remaining = Math.max(
            0,
            job.remaining - (performance.now() - job.started),
          );
        }
      }
    },
    destroy() {
      destroyed = true;
      for (const job of schedules) clearTimeout(job.timer);
      for (const event of events) {
        event.animation.cancel();
        event.item.remove();
      }
      events.clear();
      scene.remove();
    },
  };
}
