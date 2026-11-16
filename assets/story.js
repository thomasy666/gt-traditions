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
