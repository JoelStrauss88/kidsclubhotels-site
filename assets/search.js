(function () {
  'use strict';

  /* ── Data ── */
  const data = JSON.parse(document.getElementById('hotel-data').textContent);

  /* ── Elements ── */
  const resultsEl   = document.getElementById('results');
  const countEl     = document.getElementById('result-count');
  const areaEl      = document.getElementById('area');
  const countryEl   = document.getElementById('country');
  const budgetEl    = document.getElementById('budget');
  const englishEl   = document.getElementById('english-club');
  const actBtn      = document.getElementById('activities-btn');
  const actPanel    = document.getElementById('activities-panel');
  const searchBtn   = document.getElementById('search-btn');
  const rankingsEl  = document.getElementById('rankings');

  /* ── Score badge class ── */
  function scoreClass(score) {
    if (score >= 9.0) return 'score-green';
    if (score >= 8.0) return 'score-teal';
    return 'score-grey';
  }

  /* ── Base path (injected by generate.py for subdirectory hosting) ── */
  const basePath = (function() {
    const el = document.getElementById('site-base-path');
    return el ? el.textContent.trim() : '';
  })();

  /* ── Card HTML ── */
  function cardHtml(h) {
    const tags = (h.activity_tags || []).map(t => `<li class="tag">${t}</li>`).join('');
    const score = h.review_score || null;
    const scoreBadge = score ? `<span class="score-badge ${scoreClass(score)}">${score.toFixed(1)}</span>` : '';
    const budgetBadge = h.budget_tier ? `<span class="budget-badge">${h.budget_tier} · ${h.budget_est}</span>` : '';
    const img = h.image_url ? `<img class="card-img" src="${h.image_url}" alt="${h.name}" loading="lazy">` : '';
    return `
    <article class="card">
      ${img}
      <div class="card-body">
        <div class="card-meta-row">${scoreBadge}${budgetBadge}</div>
        <h3><a href="${basePath}/hotels/${h.slug}.html">${h.name}</a></h3>
        <p class="card-location">${h.subregion}, ${h.country} · ${h.area}</p>
        <ul class="tag-list">${tags}</ul>
        <p class="note">✈ ${h.airport.primary} &nbsp;·&nbsp; Kids' club: ${h.kids_club.status}</p>
      </div>
    </article>`;
  }

  /* ── Active filter values ── */
  function currentFilters() {
    const area       = areaEl    ? areaEl.value    : '';
    const country    = countryEl ? countryEl.value : '';
    const budget     = budgetEl  ? budgetEl.value  : '';
    const englishOnly = englishEl ? englishEl.checked : false;
    const activities = Array.from(
      document.querySelectorAll('input[name="activity"]:checked')
    ).map(i => i.value);
    return { area, country, budget, englishOnly, activities };
  }

  /* ── Render results ── */
  function render() {
    const { area, country, budget, englishOnly, activities } = currentFilters();

    const filtered = data.filter(h => {
      if (area    && h.area    !== area)    return false;
      if (country && h.country !== country) return false;
      if (budget  && h.budget_tier !== budget) return false;
      if (englishOnly && h.kids_club.status !== 'confirmed-english') return false;
      if (activities.length && !activities.some(a => (h.activity_tags || []).includes(a))) return false;
      return true;
    });

    if (resultsEl) {
      resultsEl.innerHTML = filtered.map(cardHtml).join('');
    }

    if (countEl) {
      if (englishOnly && filtered.length === 0) {
        countEl.textContent = `0 hotels have confirmed English-speaking kids'-club staff yet — this is being verified hotel-by-hotel. Uncheck the filter to see all ${data.length} hotels.`;
      } else {
        countEl.textContent = `${filtered.length} of ${data.length} hotels match.`;
      }
    }
  }

  /* ── Activities toggle ── */
  if (actBtn && actPanel) {
    actBtn.addEventListener('click', () => {
      const hidden = actPanel.hasAttribute('hidden');
      if (hidden) {
        actPanel.removeAttribute('hidden');
        actBtn.textContent = 'Activities ▴';
      } else {
        actPanel.setAttribute('hidden', '');
        actBtn.textContent = 'Activities ▾';
      }
    });
  }

  /* ── Search button scrolls to results ── */
  if (searchBtn) {
    searchBtn.addEventListener('click', () => {
      const sec = document.getElementById('results-section');
      if (sec) sec.scrollIntoView({ behavior: 'smooth' });
    });
  }

  /* ── Live filter on any change ── */
  document.addEventListener('change', (e) => {
    const el = e.target;
    if (
      el === areaEl || el === countryEl || el === budgetEl || el === englishEl ||
      el.name === 'activity'
    ) {
      render();
    }
  });

  /* ── Rankings ── */
  function renderRankings() {
    if (!rankingsEl) return;
    const sorted = [...data].sort((a, b) => b.review_score - a.review_score).slice(0, 8);
    rankingsEl.innerHTML = sorted.map((h, i) => {
      const cls = scoreClass(h.review_score);
      return `
        <a href="${basePath}/hotels/${h.slug}.html" style="text-decoration:none">
          <div class="rank-card">
            <div class="rank-number">#${i + 1}</div>
            <div class="rank-name">${h.name}</div>
            <div class="rank-meta">${h.subregion}</div>
            <div class="rank-bottom">
              <span class="score-badge ${cls}" style="font-size:0.9rem;padding:4px 10px;">
                ${h.review_score.toFixed(1)}
              </span>
              <span class="budget-badge">${h.budget_est || ''}</span>
            </div>
          </div>
        </a>`;
    }).join('');
  }

  /* ── Leaflet map ── */
  function initMap() {
    if (typeof L === 'undefined') return;
    const mapEl = document.getElementById('hotel-map');
    if (!mapEl) return;

    const map = L.map('hotel-map').setView([47.0, 12.0], 6);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 18
    }).addTo(map);

    // Custom green circle marker
    function greenIcon() {
      return L.divIcon({
        className: '',
        html: `<div style="
          width:28px;height:28px;
          background:#1E4035;
          border:3px solid #fff;
          border-radius:50%;
          box-shadow:0 2px 6px rgba(0,0,0,0.3);
        "></div>`,
        iconSize: [28, 28],
        iconAnchor: [14, 14],
        popupAnchor: [0, -16]
      });
    }

    data.forEach(h => {
      if (!h.lat || !h.lng) return;
      const marker = L.marker([h.lat, h.lng], { icon: greenIcon() }).addTo(map);
      marker.bindPopup(`
        <strong>${h.name}</strong><br>
        ${h.subregion}<br>
        <a href="${basePath}/hotels/${h.slug}.html">View profile &rarr;</a>
      `);
    });
  }

  /* ── Init ── */
  render();
  renderRankings();

  // Map init — wait for Leaflet if loading async
  if (typeof L !== 'undefined') {
    initMap();
  } else {
    window.addEventListener('load', initMap);
  }

})();
