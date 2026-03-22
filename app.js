(function showDate() {
  const d = new Date();
  document.getElementById("date").innerText =
    "Updated on: " + d.toLocaleDateString("en-IN", {
      year: "numeric", month: "long", day: "numeric"
    });
})();

fetch("./ai_news.json", { cache: "no-store" })
  .then(r => r.json())
  .then(items => {
    const div = document.getElementById("news");

    items.forEach(item => {
      const c = document.createElement("div");
      c.className = "card";

      c.innerHTML = `
        <div class="title">${item.title}</div>
        <div><b>Source:</b> ${item.source} • <b>Category:</b> ${item.categories.join(", ")}</div>

        <div class="section-title">Why in News</div>
        <div>${item.summary.why_in_news}</div>

        <div class="section-title">Key Facts</div>
        <div>${item.summary.key_facts}</div>

        <div class="section-title">Prelims Pointers</div>
        <div>${item.summary.prelims_pointers}</div>

        <div class="section-title">Mains Angle</div>
        <div>${item.summary.mains_angle}</div>

        <div class="section-title">Tags</div>
        <div class="tags">${item.tags.map(t => `<span>${t}</span>`).join("")}</div>
      `;
      div.appendChild(c);
    });
  })
  .catch(err => {
    console.error(err);
    document.getElementById("news").innerHTML =
      `<div class="card">Error loading data: ${err}</div>`;
  });
