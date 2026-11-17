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
