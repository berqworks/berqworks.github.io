// Signature motions for the Highlights section and hero video playback.
// Each motion plays once when it scrolls into view; click it to play again.
// With prefers-reduced-motion the final state is drawn without movement and videos stay paused.

const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

function whenVisible(el, fn, { once = true, threshold = 0.35 } = {}) {
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      fn(e.isIntersecting);
      if (e.isIntersecting && once) io.disconnect();
    }
  }, { threshold });
  io.observe(el);
}

const wait = (ms) => new Promise((r) => setTimeout(r, ms));

/* ---------- Hero video ---------- */
for (const v of document.querySelectorAll("video[data-autoplay]")) {
  if (reduced) continue;
  whenVisible(v, (visible) => {
    if (visible) { v.preload = "auto"; v.play().catch(() => {}); } else { v.pause(); }
  }, { once: false, threshold: 0.2 });
}

/* ---------- Mahjong Caravan: tiles land layer by layer ---------- */
function mahjong(box) {
  const body = box.dataset.srcBody;
  const faces = box.dataset.srcTiles.split(" ");
  // [left %, top %, layer]; a small pyramid, back to front.
  const spots = [[14, 50, 0], [38, 50, 0], [62, 50, 0], [26, 33, 1], [50, 33, 1], [38, 16, 2]];
  const tiles = spots.map(([x, y, layer], i) => {
    const t = document.createElement("div");
    t.className = "mj-tile";
    t.style.cssText = `left:${x}%;top:${y}%;z-index:${layer + 1};--layer:${layer};background-image:url(${body})`;
    const face = document.createElement("img");
    face.src = faces[i % faces.length];
    face.alt = "";
    t.append(face);
    box.append(t);
    return t;
  });
  const play = () => {
    if (reduced) { tiles.forEach((t) => t.classList.add("in")); return; }
    tiles.forEach((t) => t.classList.remove("in"));
    void box.offsetWidth;
    tiles.forEach((t) => t.classList.add("in"));
  };
  whenVisible(box, (v) => v && play());
  box.addEventListener("click", play);
}

/* ---------- Tile Swap: shuffled 3x3 picture swaps back into place ---------- */
function tileSwap(box) {
  const SWAPS = [[0, 4], [2, 6], [1, 8], [3, 5]];
  const pieces = [];
  for (let i = 0; i < 9; i++) {
    const p = document.createElement("div");
    p.className = "ts-piece";
    p.style.backgroundImage = `url(${box.dataset.src})`;
    p.style.backgroundPosition = `${(i % 3) * 50}% ${Math.floor(i / 3) * 50}%`;
    box.append(p);
    pieces.push(p);
  }
  const place = (slots) => slots.forEach((piece, cell) => {
    pieces[piece].style.left = `${(cell % 3) * 33.3333}%`;
    pieces[piece].style.top = `${Math.floor(cell / 3) * 33.3333}%`;
    pieces[piece].classList.toggle("ok", piece === cell);
  });
  const scrambled = () => {
    const slots = [...Array(9).keys()];
    for (const [a, b] of SWAPS) [slots[a], slots[b]] = [slots[b], slots[a]];
    return slots;
  };
  let running = false;
  const play = async () => {
    if (running) return;
    if (reduced) { place([...Array(9).keys()]); return; }
    running = true;
    box.classList.add("instant");
    const slots = scrambled();
    place(slots);
    void box.offsetWidth;
    box.classList.remove("instant");
    await wait(500);
    for (const [a, b] of [...SWAPS].reverse()) {
      [slots[a], slots[b]] = [slots[b], slots[a]];
      place(slots);
      await wait(520);
    }
    running = false;
  };
  place(reduced ? [...Array(9).keys()] : scrambled());
  whenVisible(box, (v) => v && play());
  box.addEventListener("click", play);
}

/* ---------- Water Sort: a faded scene colors in, region by region ---------- */
function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = src;
  });
}

async function waterSort(box) {
  const [scene, mask] = await Promise.all([loadImage(box.dataset.srcColor), loadImage(box.dataset.srcMask)]);
  const w = scene.naturalWidth, h = scene.naturalHeight;
  const canvas = document.createElement("canvas");
  canvas.width = w; canvas.height = h;
  box.append(canvas);
  const ctx = canvas.getContext("2d");

  ctx.drawImage(mask, 0, 0, w, h);
  const regions = ctx.getImageData(0, 0, w, h).data;
  ctx.drawImage(scene, 0, 0, w, h);
  const color = ctx.getImageData(0, 0, w, h);

  // Region order: every distinct gray level ascending, background (0) last.
  const levels = [...new Set(regions.filter((_, i) => i % 4 === 0))].sort((a, b) => a - b);
  const order = levels.filter((l) => l !== 0).concat(levels.includes(0) ? [0] : []);

  const faded = () => {
    const out = new ImageData(new Uint8ClampedArray(color.data), w, h);
    const d = out.data;
    for (let i = 0; i < d.length; i += 4) {
      const g = 0.3 * d[i] + 0.59 * d[i + 1] + 0.11 * d[i + 2];
      const v = g * 0.82 + 30;
      d[i] = d[i + 1] = d[i + 2] = v;
    }
    return out;
  };

  let running = false;
  const play = async () => {
    if (running) return;
    if (reduced) { ctx.putImageData(color, 0, 0); return; }
    running = true;
    const frame = faded();
    ctx.putImageData(frame, 0, 0);
    await wait(400);
    for (const level of order) {
      const d = frame.data, c = color.data;
      for (let i = 0; i < d.length; i += 4) {
        if (regions[i] === level) { d[i] = c[i]; d[i + 1] = c[i + 1]; d[i + 2] = c[i + 2]; }
      }
      ctx.putImageData(frame, 0, 0);
      await wait(level === 0 ? 0 : 120);
    }
    box.classList.add("done");
    running = false;
  };
  ctx.putImageData(reduced ? color : faded(), 0, 0);
  whenVisible(box, (v) => v && play());
  box.addEventListener("click", play);
}

const MOTIONS = { "mahjong-caravan": mahjong, "tile-swap-puzzle": tileSwap, "water-sort": waterSort };
for (const box of document.querySelectorAll(".motion[data-motion]")) {
  const fn = MOTIONS[box.dataset.motion];
  if (fn) fn(box);
}
