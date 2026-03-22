// Show today's date
(function () {
  const today = new Date();
  const opts = { year: 'numeric', month: 'long', day: 'numeric' };
  document.getElementById("date").innerText =
    "Updated on: " + today.toLocaleDateString("en-IN", opts);
})();

// Load the AI-generated JSON file
fetch("./ai_news.json", { cache: "no-store" })
  .then(r => r.json())
  .then(items => {
    const container = document.getElementById("news");
    container.innerHTML = "";

    items.forEach(item => {
      const card = document.createElement("div");
      card.className = "card";

      card.innerHTML = `
        <div class="title">${item.title}</div>
        <div><b>Source:</b> ${item.source} • ${item.published}</div>

        <div class="section-title">Why in News</div>
        <div>${item.summary.why_in_news}</div>

        <div class="section-title">Key Facts</div>
        <div>${item.summary.key_facts}</div>

        <div class="section-title">Prelims Pointers</div>
        <div>${item.summary.prelims_pointers}</div>

        <div class="section-title">Mains Angle</div>
        <div>${item.summary.mains_angle}</div>

        <div class="section-title">Tags</div>
        <div>${item.tags.map(t => `<span class="tag">${t}</span>`).join(" ")}</div>
      `;
      container.appendChild(card);
    });
  })
  .catch(err => {
    document.getElementById("news").innerHTML =
      "<div class='card'>Error loading UPSC AI news: " +
