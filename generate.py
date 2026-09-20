import json, os
from datetime import date

with open("data/hotels.json") as f:
    HOTELS = json.load(f)

SITE_NAME = "Kids Club Hotels"
BASE_URL = "https://kidsclubstay.com"
TODAY = date.today().isoformat()

AREAS = sorted(set(h["area"] for h in HOTELS))
COUNTRIES = sorted(set(h["country"] for h in HOTELS))
ALL_TAGS = sorted(set(tag for h in HOTELS for tag in h["activity_tags"]))

# GitHub Pages subdirectory prefix (empty string for custom domain root)
# Set to "/kidsclubhotels-site" when hosted at joelstrauss88.github.io/kidsclubhotels-site/
# Set to "" when hosted at kidsclubstay.com
SITE_BASE = ""

def area_slug(a):
    return a.lower().replace(" ", "-").replace("(", "").replace(")", "")

def HEAD(title, desc, canonical, extra_schema="", prefix="."):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/x-icon" href="{prefix}/assets/favicon.ico">
<link rel="icon" type="image/png" sizes="512x512" href="{prefix}/assets/favicon.png">
<link rel="apple-touch-icon" href="{prefix}/assets/favicon.png">
<link rel="stylesheet" href="{prefix}/assets/style.css">
{extra_schema}
</head>
"""

def NAV(prefix="."):
    return f"""
<header class="site-header">
  <a href="{prefix}/index.html" class="logo">{SITE_NAME}</a>
  <nav>
    <a href="{prefix}/index.html">Search</a>
    <a href="{prefix}/articles/kids-club-hotel-closures-ski-season.html">Seasonal closures guide</a>
    <a href="{prefix}/about.html">About</a>
    <a href="{prefix}/partner.html">Partner with Us</a>
  </nav>
</header>
"""

def FOOTER(prefix="."):
    top_areas = AREAS[:5]
    area_links = "\n".join(
        f'      <a href="{prefix}/regions/{area_slug(a)}.html">{a}</a>'
        for a in top_areas
    )
    return f"""
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <a href="{prefix}/index.html" class="logo">{SITE_NAME}</a>
      <p>An independent directory of family hotels with verified kids' clubs across Europe. We link to hotels' own booking pages where possible. Data on kids-club hours, staff languages, and seasonal closures is confirmed hotel-by-hotel.</p>
    </div>
    <nav class="footer-nav">
      <a href="{prefix}/index.html">Search all hotels</a>
      <a href="{prefix}/articles/kids-club-hotel-closures-ski-season.html">Seasonal closures guide</a>
      <a href="{prefix}/about.html">About</a>
      <a href="{prefix}/partner.html">Partner with Us</a>
{area_links}
    </nav>
  </div>
  <div class="footer-bottom">&copy; {date.today().year} {SITE_NAME}</div>
</footer>
"""

os.makedirs("hotels", exist_ok=True)
os.makedirs("regions", exist_ok=True)
os.makedirs("articles", exist_ok=True)

# ---------- Individual hotel pages (prefix="..") ----------
for h in HOTELS:
    prefix = ".."
    url = f"{BASE_URL}/hotels/{h['slug']}.html"
    title = f"{h['name']} — Family Hotel with Kids' Club in {h['subregion']} | {SITE_NAME}"
    desc = f"{h['name']} in {h['subregion']}, {h['country']}: kids' club details, nearest airport ({h['airport']['primary']}), activities, and seasonal closure info."
    schema = {
        "@context": "https://schema.org",
        "@type": "Hotel",
        "name": h["name"],
        "address": {"@type": "PostalAddress", "addressRegion": h["subregion"], "addressCountry": h["country"]},
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": t} for t in h["activity_tags"]],
        "url": url
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f"Does {h['name']} have a kids' club?",
             "acceptedAnswer": {"@type": "Answer", "text": f"{h['name']} is a member of {h['brand']}, an association whose hotels are required to offer supervised childcare. Specific kids'-club ages and hours for this property are {h['kids_club']['ages'].lower()} — {SITE_NAME} confirms these details directly with each hotel as partnerships are finalized."}},
            {"@type": "Question", "name": f"What is the closest airport to {h['name']}?",
             "acceptedAnswer": {"@type": "Answer", "text": f"The nearest major airport is {h['airport']['primary']}, with {h['airport']['alt']} as an alternative. {h['transport_note']}"}},
            {"@type": "Question", "name": f"When does {h['name']} close for the season?",
             "acceptedAnswer": {"@type": "Answer", "text": h["closure_note"]}},
        ]
    }

    hero_img = h.get("image_url", "")
    hero_html = f'<img class="hotel-hero-img" src="{hero_img}" alt="{h["name"]}" loading="eager">' if hero_img else ""

    score = h.get("review_score")
    review_count = h.get("review_count", 0)
    review_label = h.get("review_label", "")
    if score:
        if score >= 9.0:
            score_cls = "score-green"
        elif score >= 8.0:
            score_cls = "score-teal"
        else:
            score_cls = "score-grey"
        score_html = f'<span class="score-badge {score_cls}">{score:.1f}<span class="score-label">{review_label}</span></span>'
        review_note = f'<p class="note">Based on {review_count:,} guest reviews</p>'
    else:
        score_html = ""
        review_note = ""

    budget_tier = h.get("budget_tier", "")
    budget_est = h.get("budget_est", "")
    budget_html = f'<span class="budget-badge">{budget_tier} · {budget_est}</span>' if budget_tier else ""

    html = HEAD(title, desc, url, f'<script type="application/ld+json">{json.dumps(schema)}</script>\n<script type="application/ld+json">{json.dumps(faq)}</script>', prefix=prefix) + f"""<body>
{NAV(prefix)}
<main class="hotel-profile">
  <p class="breadcrumb"><a href="{prefix}/index.html">Search</a> &rsaquo; <a href="{prefix}/regions/{area_slug(h['area'])}.html">{h['area']}</a> &rsaquo; {h['name']}</p>
  {hero_html}
  <h1>{h['name']}</h1>
  <div class="hotel-hero-row">
    {score_html}
    {budget_html}
    <span class="meta">{h['subregion']}, {h['country']} &middot; {h['brand']} &middot; Tier: {h['quality_tier']}</span>
  </div>
  {review_note}

  <section>
    <h2>Activities &amp; features</h2>
    <ul class="tag-list">
      {''.join(f'<li class="tag">{t}</li>' for t in h['activity_tags'])}
    </ul>
  </section>

  <section>
    <h2>Kids' club</h2>
    <table class="fact-table">
      <tr><th>Age range</th><td>{h['kids_club']['ages']}</td></tr>
      <tr><th>Hours</th><td>{h['kids_club']['hours']}</td></tr>
      <tr><th>Staff languages</th><td>{h['kids_club']['staff_languages']}</td></tr>
    </table>
    <p class="note">Status: {h['kids_club']['status']}. {SITE_NAME} verifies these fields directly with each hotel — see our <a href="{prefix}/articles/kids-club-hotel-closures-ski-season.html">data verification notes</a>.</p>
  </section>

  <section>
    <h2>Getting there</h2>
    <table class="fact-table">
      <tr><th>Nearest airport</th><td>{h['airport']['primary']}</td></tr>
      <tr><th>Alternative airport</th><td>{h['airport']['alt']}</td></tr>
      <tr><th>Recommended transport</th><td>{h['transport_note']}</td></tr>
    </table>
  </section>

  <section>
    <h2>Seasonal closures</h2>
    <p>{h['closure_note']}</p>
  </section>

  <section>
    <h2>Book</h2>
    <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-bottom:12px">
      <a class="cta" href="{h['profile_source']}" rel="nofollow sponsored">View on hotel website &rarr;</a>
      {('<a class="cta" style="background:#003580" href="' + h['booking_com_url'] + '" rel="nofollow sponsored">Check on Booking.com &rarr;</a>') if h.get('booking_com_url') else ''}
    </div>
    <p class="note">Booking.com link includes our affiliate tag — this supports the directory at no cost to you. We recommend checking the hotel&rsquo;s own website too, as direct rates are sometimes lower.</p>
  </section>
</main>
{FOOTER(prefix)}
</body></html>"""
    with open(f"hotels/{h['slug']}.html", "w") as f:
        f.write(html)

# ---------- Region hub pages (prefix="..") ----------
for area in AREAS:
    prefix = ".."
    hotels_in_area = [h for h in HOTELS if h["area"] == area]
    url = f"{BASE_URL}/regions/{area_slug(area)}.html"
    title = f"Family Hotels with Kids' Clubs in {area} | {SITE_NAME}"
    desc = f"Browse {len(hotels_in_area)} verified family hotels with kids' clubs in {area}, with nearest airport, transport, and seasonal closure info for each."
    cards = "".join(f"""
      <article class="card">
        {'<img class="card-img" src="' + h['image_url'] + '" alt="' + h['name'] + '" loading="lazy">' if h.get('image_url') else ''}
        <div class="card-body">
          <div class="card-meta-row">
            {'<span class="score-badge ' + ('score-green' if h.get('review_score', 0) >= 9 else 'score-teal' if h.get('review_score', 0) >= 8 else 'score-grey') + '">' + f"{h['review_score']:.1f}" + '</span>' if h.get('review_score') else ''}
            {'<span class="budget-badge">' + h['budget_tier'] + ' · ' + h['budget_est'] + '</span>' if h.get('budget_tier') else ''}
          </div>
          <h3><a href="{prefix}/hotels/{h['slug']}.html">{h['name']}</a></h3>
          <p class="card-location">{h['subregion']}, {h['country']}</p>
          <ul class="tag-list">{''.join(f'<li class="tag">{t}</li>' for t in h['activity_tags'])}</ul>
          <p class="note">&#x2708; {h['airport']['primary']}</p>
        </div>
      </article>""" for h in hotels_in_area)
    html = HEAD(title, desc, url, prefix=prefix) + f"""<body>
{NAV(prefix)}
<main>
  <p class="breadcrumb"><a href="{prefix}/index.html">Search</a> &rsaquo; {area}</p>
  <h1>Family hotels with kids' clubs in {area}</h1>
  <p>{area} is home to {len(hotels_in_area)} hotels in our directory that belong to verified family-hotel associations and offer supervised kids' clubs. Use the filters on the <a href="{prefix}/index.html">search page</a> to narrow by activity, budget, or nearest airport.</p>
  <div class="card-grid">{cards}</div>
</main>
{FOOTER(prefix)}
</body></html>"""
    with open(f"regions/{area_slug(area)}.html", "w") as f:
        f.write(html)

# ---------- Homepage with hero + search UI (prefix=".") ----------
prefix = "."
hotel_json = json.dumps(HOTELS)
areas_options = "".join(f'<option value="{a}">{a}</option>' for a in AREAS)
countries_options = "".join(f'<option value="{c}">{c}</option>' for c in COUNTRIES)
tag_checkboxes = "".join(
    f'<label><input type="checkbox" name="activity" value="{t}"> {t}</label>'
    for t in ALL_TAGS
)

itemlist_schema = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "itemListElement": [
        {"@type": "ListItem", "position": i+1, "url": f"{BASE_URL}/hotels/{h['slug']}.html", "name": h["name"]}
        for i, h in enumerate(HOTELS)
    ]
}

index_html = HEAD(
    f"Kids Club Hotels — Find Family Hotels with Real Kids' Clubs in Europe",
    "Kids Club Hotels is an independent directory of European family hotels with verified kids' clubs. Search by location, nearest airport, English-speaking childcare, and activities like skiing or cycling.",
    f"{BASE_URL}/index.html",
    f'<script type="application/ld+json">{json.dumps(itemlist_schema)}</script>',
    prefix=prefix
) + f"""<body>
{NAV(prefix)}

<!-- ── HERO ── -->
<section class="hero">
  <svg class="hero-mountain" viewBox="0 0 1440 320" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <path fill="#ffffff" d="M0,320 L0,220 L80,180 L140,210 L200,130 L280,160 L360,80 L440,120 L520,60 L600,100 L660,40 L720,90 L780,30 L840,80 L920,50 L980,110 L1060,70 L1140,130 L1200,90 L1280,150 L1360,110 L1440,170 L1440,320 Z"/>
    <path fill="#ffffff" opacity="0.4" d="M0,320 L0,260 L120,240 L200,260 L320,200 L420,230 L540,180 L620,210 L720,160 L820,200 L920,170 L1020,210 L1120,185 L1220,220 L1320,195 L1440,225 L1440,320 Z"/>
  </svg>

  <div class="hero-content">
    <h1>Find family hotels with real kids&apos; clubs across Europe</h1>
    <p class="hero-sub">{len(HOTELS)} verified hotels &middot; Alps, Italy, France &amp; more &middot; Filter by budget, activities &amp; airport</p>

    <div class="search-bar-wrap">
      <select id="area" name="area" aria-label="Location">
        <option value="">All of Europe</option>
        {areas_options}
      </select>

      <select id="country" name="country" aria-label="Country">
        <option value="">Any country</option>
        {countries_options}
      </select>

      <select id="budget" name="budget" aria-label="Budget">
        <option value="">Any budget</option>
        <option value="€">&euro; Budget</option>
        <option value="€€">&euro;&euro; Mid-range</option>
        <option value="€€€">&euro;&euro;&euro; Premium</option>
      </select>

      <button type="button" class="activities-btn" id="activities-btn">Activities &#9660;</button>
      <button type="button" class="search-btn" id="search-btn">Search &rarr;</button>
    </div>

    <div class="activities-panel" id="activities-panel" hidden>
      <p class="panel-title">Filter by activities</p>
      <div class="activities-grid">
        {tag_checkboxes}
      </div>
    </div>

    <label class="english-toggle">
      <input type="checkbox" id="english-club">
      English-speaking kids&apos; club staff only
    </label>
  </div>
</section>

<!-- ── RESULTS ── -->
<section class="results-section" id="results-section">
  <div class="section-inner">
    <p id="result-count" class="note"></p>
    <div id="results" class="card-grid"></div>
  </div>
</section>

<!-- ── RANKINGS ── -->
<section class="rankings-section">
  <div class="section-inner">
    <h2>Top Rated Hotels</h2>
    <p class="section-sub">Ranked by aggregated guest reviews</p>
    <div class="rankings-scroll" id="rankings"></div>
  </div>
</section>

<!-- ── MAP ── -->
<section class="map-section">
  <div class="section-inner">
    <h2>Explore on the Map</h2>
    <p class="section-sub">Click any pin to view the hotel profile</p>
  </div>
  <div id="hotel-map"></div>
</section>

<!-- ── BLOG ── -->
<section class="blog-section">
  <div class="section-inner">
    <h2>From the Blog</h2>
    <p class="section-sub">Guides to help you plan the perfect family hotel stay</p>
    <div class="blog-grid">

      <article class="blog-card">
        <p class="blog-category">Seasonal Planning</p>
        <h3>When Do Alpine Family Hotels Close?</h3>
        <p>Many Alpine family hotels shut for 1&ndash;3 weeks between ski season and summer. Here&rsquo;s why it happens and a hotel-by-hotel closure tracker to save you a wasted trip.</p>
        <a class="read-more" href="{prefix}/articles/kids-club-hotel-closures-ski-season.html">Read guide &rarr;</a>
      </article>

      <article class="blog-card">
        <p class="blog-category">Kids&apos; Clubs</p>
        <h3>How to Choose the Right Kids&apos; Club Age Range</h3>
        <p>Not all kids&apos; clubs cater to every age. We break down what to look for when your children are under 2, 2&ndash;6, or 7+ &mdash; and which hotels in our directory do each age group best.</p>
        <a class="read-more" href="#">Read guide &rarr;</a>
      </article>

      <article class="blog-card">
        <p class="blog-category">Trip Planning</p>
        <h3>Ski Season vs. Summer: Which is Better for Families?</h3>
        <p>Both seasons have their merits. Ski season means snow and cosy evenings; summer offers hiking, lakes and cheaper rates. Here&rsquo;s how to decide based on your children&rsquo;s ages.</p>
        <a class="read-more" href="#">Read guide &rarr;</a>
      </article>

    </div>
  </div>
</section>

<!-- ── CONTACT ── -->
<section class="contact-section">
  <div class="section-inner">
    <h2>Get in Touch</h2>
    <p>Questions about a hotel, partnership enquiries, or data corrections &mdash; email us at <a href="mailto:hello@kidsclubstay.com">hello@kidsclubstay.com</a></p>
  </div>
</section>

{FOOTER(prefix)}

<!-- ── DATA ── -->
<script id="site-base-path" type="text/plain">{SITE_BASE}</script>
<script id="hotel-data" type="application/json">{hotel_json}</script>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="{prefix}/assets/search.js"></script>
</body></html>"""

with open("index.html", "w") as f:
    f.write(index_html)

# ---------- About page ----------
prefix = "."
about_html = HEAD(
    f"About | {SITE_NAME}",
    "Kids Club Hotels is an independent directory of European family hotels with verified kids' clubs, built for parents who want real, confirmed information rather than marketing copy.",
    f"{BASE_URL}/about.html",
    prefix=prefix
) + f"""<body>
{NAV(prefix)}
<main class="static-page">
  <h1>About Kids Club Hotels</h1>
  <p>Kids Club Hotels is an independent directory of European family hotels with verified kids' clubs. It exists for one reason: parents planning a family holiday need real, confirmed information &mdash; not marketing copy. Every hotel in this directory belongs to a recognised family-hotel association (Kinderhotels Europa, Familienhotels S&uuml;dtirol, Center Parcs Europe, or Familotel) and offers supervised childcare. We confirm the specifics &mdash; hours, age ranges, staff languages &mdash; directly with each property.</p>

  <h2>How we verify</h2>
  <p>Kids-club hours, age ranges, and staff languages are confirmed directly with hotel staff, not scraped from booking platforms or taken from brochure copy. Where a detail has not yet been confirmed with the property, we say so explicitly &mdash; fields marked &ldquo;not yet confirmed&rdquo; reflect that in-progress state, not a gap in our data. We update listings as confirmations come in and as seasonal operations change.</p>

  <h2>Contact</h2>
  <p>For hotel listings, corrections, or partnerships: <a href="mailto:hello@kidsclubstay.com">hello@kidsclubstay.com</a></p>
</main>
{FOOTER(prefix)}
</body></html>"""

with open("about.html", "w") as f:
    f.write(about_html)

# ---------- Partner with Us page ----------
prefix = "."
partner_html = HEAD(
    f"Partner with Us | {SITE_NAME}",
    "Hotels with verified kids' clubs: list your property on Kids Club Hotels and earn qualified family bookings through a simple referral fee arrangement.",
    f"{BASE_URL}/partner.html",
    prefix=prefix
) + f"""<body>
{NAV(prefix)}
<main class="static-page">
  <h1>Partner with Kids Club Hotels</h1>
  <p>We list hotels with verified kids' clubs across Europe. If families find your hotel through our directory and book, we&rsquo;d like to earn a small referral fee &mdash; here&rsquo;s how it works.</p>

  <h2>What we offer</h2>
  <ul>
    <li>A detailed, verified listing covering kids&rsquo;-club hours, age ranges, staff languages, and activities</li>
    <li>Transport and nearest-airport information so families can plan their journey</li>
    <li>A direct booking link to your own website (not an OTA)</li>
    <li>Inclusion in our email newsletter and social content when relevant</li>
    <li>Priority placement in search results and regional guides for confirmed partners</li>
  </ul>

  <h2>What we ask</h2>
  <p>A referral fee of 5&ndash;8% on completed bookings that originate from Kids Club Hotels, or a flat monthly listing fee &mdash; we&rsquo;re flexible on structure depending on what works for your property. We prefer direct arrangements over routing through an OTA, which keeps the cost lower for both sides and keeps the booking relationship with you.</p>

  <h2>Get in touch</h2>
  <p>Email <a href="mailto:hello@kidsclubstay.com">hello@kidsclubstay.com</a> with your hotel name and a brief note about your kids&rsquo; club. We&rsquo;ll follow up within 2 business days.</p>
</main>
{FOOTER(prefix)}
</body></html>"""

with open("partner.html", "w") as f:
    f.write(partner_html)

print(f"Generated: {len(HOTELS)} hotel pages, {len(AREAS)} region pages, 1 homepage, about.html, partner.html")
