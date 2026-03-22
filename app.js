// 1) Show today's date
(function () {
  const today = new Date();
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  const el = document.getElementById("date");
  if (el) el.innerText = "Updated on: " + today.toLocaleDateString("en-IN", options);
})();

// 2) Load local news.json and render cards
(function () {
  const container = document.getElementById("news");
  if (!container) return;

  fetch("./news.json", { cache: "no-store" })
    .then(r => {
      if (!r.ok) throw new Error(`news.json HTTP ${r.status}`);
      return r.json();
    })
    .then(items => {
      if (!Array.isArray(items) || items.length === 0) {
        container.innerHTML = `<div class="news-item"><b>No news found</b><br>news.json is empty.</div>`;
        return;
      }
      container.innerHTML = "";
      items.forEach(item => {
        const div = document.createElement("div");
        div.className = "news-item";
        const title = item.title ?? "";
        const summary = item.summary ?? "";
        const link = item.link ?? "";
        div.innerHTML = link
          ? `<b><a href="${link}" target="_blank" rel="noopener">${title}</a></b><br>${summary}`
          : `<b>${title}</b><br>${summary}`;
        container.appendChild(div);
      });
    })
    .catch(err => {
      console.error("Failed to load news.json:", err);
      container.innerHTML =
        `<div class="news-item"><b>Could not load news.json</b><br>${err.message}</div>`;
    });
})();
