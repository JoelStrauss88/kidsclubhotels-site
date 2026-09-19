(function () {
  const data = JSON.parse(document.getElementById('hotel-data').textContent);
  const resultsEl = document.getElementById('results');
  const countEl = document.getElementById('result-count');
  const form = document.getElementById('filters');

  function cardHtml(h) {
    const tags = h.activity_tags.map(t => `<li class="tag">${t}</li>`).join('');
    return `
      <article class="card">
        <h3><a href="/hotels/${h.slug}.html">${h.name}</a></h3>
        <p>${h.subregion}, ${h.country} &middot; ${h.area}</p>
        <ul class="tag-list">${tags}</ul>
        <p class="note">Nearest airport: ${h.airport.primary} &middot; Kids' club: ${h.kids_club.status}</p>
      </article>`;
  }

  function currentFilters() {
    const area = document.getElementById('area').value;
    const country = document.getElementById('country').value;
    const englishOnly = document.getElementById('english-club').checked;
    const activities = Array.from(form.querySelectorAll('input[name="activity"]:checked')).map(i => i.value);
    return { area, country, englishOnly, activities };
  }

  function render() {
    const { area, country, englishOnly, activities } = currentFilters();
    const filtered = data.filter(h => {
      if (area && h.area !== area) return false;
      if (country && h.country !== country) return false;
      if (englishOnly && h.kids_club.status !== 'confirmed-english') return false;
      if (activities.length && !activities.some(a => h.activity_tags.includes(a))) return false;
      return true;
    });
    resultsEl.innerHTML = filtered.map(cardHtml).join('');
    countEl.textContent = englishOnly && filtered.length === 0
      ? `0 hotels have confirmed English-speaking kids'-club staff yet — this is being verified hotel-by-hotel. Uncheck the filter to see all ${data.length} hotels.`
      : `${filtered.length} of ${data.length} hotels match.`;
  }

  form.addEventListener('change', render);
  render();
})();
