for (const compare of document.querySelectorAll("[data-compare]")) {
  const control = compare.querySelector("input[type=range]");
  const frame = compare.querySelector(".compare-frame");

  const update = () => frame.style.setProperty("--reveal", control.value + "%");
  control.addEventListener("input", update);
  update();
}

for (const flip of document.querySelectorAll("[data-cap]")) {
  const trigger = flip.querySelector("button");
  const front = flip.querySelector("[data-front]");
  const back = flip.querySelector("[data-back]");

  trigger.addEventListener("click", () => {
    const showBack = back.hidden;
    front.hidden = showBack;
    back.hidden = !showBack;
    trigger.setAttribute("aria-pressed", String(showBack));
  });
}

for (const timeline of document.querySelectorAll("[data-timeline]")) {
  const list = timeline.querySelector(".timeline-list");
  const items = [...list.children];
  const dots = items.map((item) => item.querySelector(".timeline-dot"));
  const steps = timeline.querySelector(".timeline-steps");
  const count = steps.querySelector(".timeline-count");
  const [earlier, later] = steps.querySelectorAll("button");
  let current = 0;

  const select = (index, focus = false) => {
    current = Math.max(0, Math.min(items.length - 1, index));
    items.forEach((item, i) => {
      item.classList.toggle("is-current", i === current);
      item.classList.toggle("is-past", i < current);
      dots[i].setAttribute("aria-expanded", String(i === current));
    });
    list.style.setProperty("--progress", items[current].style.getPropertyValue("--pos"));
    count.textContent = `${current + 1} of ${items.length}`;
    earlier.disabled = current === 0;
    later.disabled = current === items.length - 1;
    if (focus) dots[current].focus();
  };

  dots.forEach((dot, index) => {
    dot.hidden = false;
    dot.addEventListener("click", () => select(index));
    dot.addEventListener("keydown", (event) => {
      const target = { ArrowLeft: current - 1, ArrowRight: current + 1, Home: 0, End: items.length - 1 }[event.key];
      if (target === undefined) return;
      event.preventDefault();
      select(target, true);
    });
  });
  earlier.addEventListener("click", () => select(current - 1));
  later.addEventListener("click", () => select(current + 1));

  steps.hidden = false;
  timeline.classList.add("is-line");
  select(0);
}

const STUNT_FONT = {
  G: [".####", "#....", "#.###", "#...#", ".###."],
  T: ["#####", "..#..", "..#..", "..#..", "..#.."],
  E: ["#####", "#....", "####.", "#....", "#####"],
  C: [".####", "#....", "#....", "#....", ".####"],
  H: ["#...#", "#...#", "#####", "#...#", "#...#"],
};

for (const stunt of document.querySelectorAll("[data-stunt]")) {
  const COLS = 25;
  const ROWS = 7;
  const stands = stunt.querySelector(".stunt-stands");
  const controls = stunt.querySelector(".stunt-controls");
  const buttons = [...controls.querySelectorAll("[data-word]")];
  const status = stunt.querySelector(".stunt-status");
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const cards = [];
  let waveTimers = [];

  for (let i = 0; i < COLS * ROWS; i++) {
    const card = document.createElement("span");
    card.className = "stunt-card";
    card.innerHTML = '<span class="stunt-face stunt-front"></span><span class="stunt-face stunt-back"></span>';
    stands.append(card);
    cards.push(card);
  }

  const pattern = (word) => {
    const lit = new Set();
    const width = word.length * 6 - 1;
    const left = Math.floor((COLS - width) / 2);
    [...word].forEach((letter, n) => {
      STUNT_FONT[letter].forEach((line, row) => {
        [...line].forEach((cell, col) => {
          if (cell === "#") lit.add((row + 1) * COLS + left + n * 6 + col);
        });
      });
    });
    return lit;
  };

  const clearWave = () => {
    waveTimers.forEach(clearTimeout);
    waveTimers = [];
  };

  const press = (active) => buttons.forEach((b) => b.setAttribute("aria-pressed", String(b === active && b.dataset.word !== "")));

  const show = (word, button) => {
    clearWave();
    press(button);
    if (word === "WAVE") {
      cards.forEach((card) => { card.style.removeProperty("--delay"); card.classList.remove("is-up", "is-gold"); });
      for (let col = 0; col < COLS; col++) {
        const column = cards.filter((_, i) => i % COLS === col);
        waveTimers.push(setTimeout(() => column.forEach((c) => c.classList.add("is-up", "is-gold")), col * 70));
        waveTimers.push(setTimeout(() => column.forEach((c) => c.classList.remove("is-up", "is-gold")), col * 70 + 520));
      }
      waveTimers.push(setTimeout(() => press(null), COLS * 70 + 600));
      status.textContent = "The wave rolls across the section.";
      return;
    }
    const lit = pattern(word);
    cards.forEach((card, i) => {
      card.style.setProperty("--delay", reduceMotion ? "0s" : `${(i % COLS) * 0.022 + Math.floor(i / COLS) * 0.03}s`);
      card.classList.toggle("is-up", word !== "");
      card.classList.toggle("is-gold", lit.has(i));
    });
    status.textContent = word ? `The section spells ${word}.` : "Cards down.";
  };

  buttons.forEach((button) => button.addEventListener("click", () => show(button.dataset.word, button)));

  stands.addEventListener("click", (event) => {
    const card = event.target.closest(".stunt-card");
    if (!card) return;
    clearWave();
    press(null);
    card.style.setProperty("--delay", "0s");
    const gold = !card.classList.contains("is-gold");
    card.classList.add("is-up");
    card.classList.toggle("is-gold", gold);
    status.textContent = "Drawing your own display.";
  });

  controls.hidden = false;
  status.textContent = "";
}

{
  const imageLinks = [...document.querySelectorAll("a[href]")].filter((link) => /\.(webp|png|jpe?g|gif)(\?.*)?$/i.test(link.getAttribute("href")) && link.querySelector("img"));
  if (imageLinks.length && typeof HTMLDialogElement === "function") {
    const viewer = document.createElement("dialog");
    viewer.className = "lightbox";
    viewer.setAttribute("aria-label", "Image viewer");
    viewer.innerHTML = '<button type="button" class="lightbox-close" aria-label="Close image">✕</button><figure><img alt=""><figcaption></figcaption></figure>';
    document.body.append(viewer);
    const image = viewer.querySelector("img");
    const caption = viewer.querySelector("figcaption");
    let opener = null;

    const close = () => viewer.close();
    viewer.querySelector(".lightbox-close").addEventListener("click", close);
    viewer.addEventListener("click", (event) => { if (event.target === viewer) close(); });
    viewer.addEventListener("close", () => { image.removeAttribute("src"); document.documentElement.classList.remove("lightbox-open"); opener?.focus(); });

    for (const link of imageLinks) {
      link.addEventListener("click", (event) => {
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) return;
        event.preventDefault();
        opener = link;
        const thumb = link.querySelector("img");
        image.src = link.href;
        image.alt = thumb.alt;
        const source = link.closest("figure")?.querySelector("figcaption");
        caption.innerHTML = source ? source.innerHTML : "";
        caption.hidden = !source;
        document.documentElement.classList.add("lightbox-open");
        viewer.showModal();
      });
    }
  }
}

{
  const externalLinks = [...document.querySelectorAll('a[href^="http"]')];
  if (externalLinks.length && typeof HTMLDialogElement === "function" && typeof qrcode === "function") {
    const sheet = document.createElement("dialog");
    sheet.className = "lightbox";
    sheet.setAttribute("aria-labelledby", "qr-heading");
    sheet.innerHTML = `<button type="button" class="lightbox-close" aria-label="Close">✕</button>
      <div class="qr-panel">
        <h2 id="qr-heading">Scan to read more</h2>
        <p>Point your phone’s camera at the code to open this page.</p>
        <div class="qr-code"></div>
        <p class="qr-title"></p>
        <p class="qr-url"></p>
        <button type="button" class="qr-back">Back to the story</button>
      </div>`;
    document.body.append(sheet);
    const code = sheet.querySelector(".qr-code");
    const title = sheet.querySelector(".qr-title");
    const url = sheet.querySelector(".qr-url");

    const close = () => sheet.close();
    sheet.querySelector(".lightbox-close").addEventListener("click", close);
    sheet.querySelector(".qr-back").addEventListener("click", close);
    sheet.addEventListener("click", (event) => { if (event.target === sheet) close(); });
    sheet.addEventListener("close", () => document.documentElement.classList.remove("lightbox-open"));

    for (const link of externalLinks) {
      link.addEventListener("click", (event) => {
        event.preventDefault();
        const qr = qrcode(0, "M");
        qr.addData(link.href);
        qr.make();
        code.innerHTML = qr.createSvgTag({ cellSize: 4, margin: 0, scalable: true });
        title.textContent = link.textContent.trim();
        url.textContent = link.hostname + link.pathname.replace(/\/$/, "");
        document.documentElement.classList.add("lightbox-open");
        sheet.showModal();
      });
    }
  }
}
